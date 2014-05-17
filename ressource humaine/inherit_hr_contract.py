# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time



class inherit_hr_contract(osv.osv):
    
    _name ='hr.contract' 
    
    _inherit = 'hr.contract'
    
    #fonction qui vérifie la saisie du salaire lors d'un click (Onchange)
    def onchange_salary(self,cr,uid,ids,salary):
        if str(salary).isdigit():
            return True
        else:    
            raise osv.except_osv(_('Invalid salary'), _('Please enter a valid salary'))

    
    def _get_contract_occupation_rate(self, cr, uid, ids, field_name, args, context=None):
        result = {}        
        for i in ids:            
            sql_req =""" SELECT occupation_rate AS occupation_rate
                         FROM cost_center
                         WHERE contract_id=%d                                                  
                         """ % (i,)
#                      AND cost_center.active = TRUE
            cr.execute(sql_req)
            sql_res = cr.dictfetchall()
            result[i]=0
            if sql_res:                
                for lign in sql_res:
                    result[i] += lign['occupation_rate']                 
        return result 
     
    def onchange_cost_center(self,cr,uid,ids,cost_center):                    
        occupation_rate = 0
        for cost_center_details in cost_center:                        
            occupation_rate += cost_center_details[2]['occupation_rate']
                        
        res={
                'value':{
                         'occupation_rate': occupation_rate,
                         
        
                         },
             }
        if occupation_rate > 100: 
            res['warning']={
                            'title': 'Occupation rate is incorrect',
                            'message': 'The occupation rate has exceed 100% Please check the associated cost center',
                            }
                
        return res
    
    def _check_occupation_rate(self, cr,uid,ids,context=None):
#        if self._get_contract_occupation_rate(self, cr, uid, ids, 'occupation_rate', None, context=context) > 100:
        state = True
        contracts = self.browse(cr,uid,ids,context=context)
        for contract in contracts:
            occupation_rate = contract.occupation_rate            
            if occupation_rate > 100:
                state = False
        return state
    
    def onchange_employee_id(self,cr,uid,ids,employee_id,occupation_rate,boolean=False):                                                
        sql_req="""SELECT occupation_rate
                   FROM hr_contract
                   WHERE employee_id = %d
                   AND id <>  %d
                   """ %(employee_id,ids[0],)
        cr.execute(sql_req)
        sql_res = cr.dictfetchall()
        if not sql_res:
            return True
        if sql_res[0]['occupation_rate'] is None:
            return True
        employee_occupation_rate=occupation_rate
        for lign in sql_res:
            if lign['occupation_rate'] is None:
                continue
            else:
                employee_occupation_rate += int(lign['occupation_rate'])
        if employee_occupation_rate > 100:
            if boolean:
                return False
            else:
                res={
                     'warning':{
                                'title': 'Cannot associate this contract with the chosen employee',
                                'message': 'The total of occupation rate has exceed 100%',
                                }
                 }            
                return res
        else:
            return True
    
    def _check_employee_id(self, cr,uid,ids,context=None):
        contracts = self.browse(cr,uid,ids,context=context)
        for contract in contracts:
            occupation_rate = int(contract.occupation_rate)
            employee_id=contract.employee_id._id
            if self.onchange_employee_id(cr,uid,ids,employee_id,occupation_rate,True):
                return True
            else:
                return False
            
    
    def _get_contract_status(self, cr, uid, ids, field_name, args, context=None):
        result = {}        
        for i in ids:            
            sql_req =""" SELECT date_end  
                         FROM hr_contract
                         WHERE contract_id=%d
                         AND active = TRUE                                                  
                         """ % (i,)                      
            cr.execute(sql_req)
            sql_res = cr.dictfetchall()
            result[i]=0
            if not sql_res:
                return True
            if sql_res:                
                for lign in sql_res:
                    if lign['date_end'] is None:
                        continue 
                                     
        return result
                
        
        
        
    
#     def _get_cost_center(self, cr, uid, ids, field_name, arg, context):
#         result = {}
#         for i in ids:
#             contract = self.browse(cr,uid,i,context=context)
#             occupation_rate = int(contract.occupation_rate)
#             sql_req =""" SELECT id AS id
#                          FROM cost_center
#                          WHERE (%d + cost_center.occupation_rate <= 100)
#                          
#                          
#                          """ % (occupation_rate,)
# #                      AND cost_center.active = TRUE
#             cr.execute(sql_req)
#             sql_res = cr.dictfetchall()
#             result[i]=[]
#             if sql_res:                
#                 for lign in sql_res:
#                     result[i].append(lign['id'])                 
#         return result         
#         
#     def _save_cost_center(self, cr, uid, ids, field_name, field_value, arg, context):
#         self.pool.get('cost.center').write(cr, uid, field_name,{'cost_center_ids': field_value}, context=context)
    
    _columns = { 
                'salary': fields.float('Salary',required=True),
                'salary_type_id':fields.many2one('salary.type', 'Salary type', required=True),                 
                
                'work_time_type':fields.selection([
                     ('complete','Complete'),
                     ('partial','Partial'),
                     ],'Working time type', select=True),
                'active': fields.boolean('Active'),
                'occupation_rate': fields.function(_get_contract_occupation_rate, string='Occupation rate', type='integer', help='Occupation rate calculated based on the cost center related to this contract',readonly=True,store=True),
                'taxed_at_source':fields.boolean('Taxed at source', required=False),
                'cost_center_ids': fields.one2many('cost.center', 'contract_id', 'Cost centers'),

                #'cost_center_ids':fields.many2many('cost.center','contract_cost_center_rel',  'hr_contract_id','cost_center_id',  'Cost centers'),
                #'contract_cost_center_rel', 'hr_contract_id', 'cost_center_id',
                #'filter_cost_center',fnct_inv=_save_cost_center
                #'cost_center_ids':fields.function(_get_cost_center,type='many2many',store=True,obj="cost.center",method=True,string='Cost centers'),                
    
                #juste pour eviter le problème de contraint not null sur wage 
                #'wage': fields.float('Wage', digits=(16,2), required=True, help="Basic Salary of the employee"),  
    }            
    
    _defaults = {
                 'wage':0,
                 'active': 0,
        }
    
    _constraints = [
                    (_check_occupation_rate, 'The occupation rate has exceed 100% Please check the associated cost center', ['occupation_rate']),
                    (_check_employee_id, 'Cannot associate this contract with the chosen employee', ['employee_id'])
                ]
    

    
inherit_hr_contract()  