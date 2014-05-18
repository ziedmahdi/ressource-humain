# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import datetime 
from datetime import date





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
        occupation_rate =0
        current_date = date.today()        
        contract = self.browse(cr,uid,ids[0],context=context)
        cost_center = contract.cost_center_ids
        for cost_center_details in cost_center:                                   
            date_start =datetime.datetime.strptime(cost_center_details.date_entry, "%Y-%m-%d").date()
            date_end =datetime.datetime.strptime(cost_center_details.date_release, "%Y-%m-%d").date()
            if date_end >= current_date and current_date >= date_start:            
                occupation_rate +=   cost_center_details.occupation_rate        
        result[ids[0]] =  occupation_rate                                                                                        
        return result 

# à changer
    def onchange_cost_center(self,cr,uid,ids,cost_center):                    
        occupation_rate = 0
        current_date = date.today()
        for cost_center_details in cost_center:                                
            date_start =datetime.datetime.strptime(cost_center_details[2]['date_entry'], "%Y-%m-%d").date()
            date_end =datetime.datetime.strptime(cost_center_details[2]['date_release'], "%Y-%m-%d").date()
            if date_end >= current_date and current_date >= date_start:                       
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
        occupation_rate=0
        contracts = self.browse(cr,uid,ids,context=context)
        current_date = date.today()
        for contract in contracts:
            cost_center = contract.cost_center_ids
            for cost_center_details in cost_center:                                   
                date_start =datetime.datetime.strptime(cost_center_details.date_entry, "%Y-%m-%d").date()
                date_end =datetime.datetime.strptime(cost_center_details.date_release, "%Y-%m-%d").date()
                if date_end >= current_date and current_date >= date_start:            
                    occupation_rate +=   cost_center_details.occupation_rate  
        if occupation_rate > 100:            
            return False
        return True
    
    def onchange_employee_id(self,cr,uid,ids,employee_id,occupation_rate,boolean=False):                                                
        sql_req="""SELECT occupation_rate
                   FROM hr_contract
                   WHERE employee_id = %d                   
                   """ %(employee_id,)
        if ids:
            sql_req += """AND id <>  %d"""%(ids[0],)
        cr.execute(sql_req)
        sql_res = cr.dictfetchall()
        if not sql_res:
            return True #even if the contract occupation rate is greater than 100%         
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
            
#a changer    
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
    
    def _get_date_end(self, cr, uid, ids, field_name, args, context=None):
        result = {}
        current_date = date.today()
        contract = self.browse(cr,uid,ids[0],context=context)
        date_max= current_date             
        cost_center = contract.cost_center_ids
        for cost_center_details in cost_center:
            date_entry=cost_center_details.date_entry
            date_release=cost_center_details.date_release                                    
            date_start =datetime.datetime.strptime(date_entry, "%Y-%m-%d").date()
            date_end =datetime.datetime.strptime(date_release, "%Y-%m-%d").date()
            if date_end >= current_date and current_date >= date_start: 
                if date_max < date_end:
                    date_max = date_end
        result[ids[0]] = date_max                                  
        return result
    
    def _get_date_start(self, cr, uid, ids, field_name, args, context=None):
        result = {}
        for i in ids:
            contract = self.browse(cr,uid,i,context=context)
            date_min= current_date = date.today()            
            cost_center = contract.cost_center_ids
            for cost_center_details in cost_center:
                date_entry=cost_center_details.date_entry
                date_release=cost_center_details.date_release                                    
                date_start =datetime.datetime.strptime(date_entry, "%Y-%m-%d").date()
                date_end =datetime.datetime.strptime(date_release, "%Y-%m-%d").date()
                if date_end >= current_date and current_date >= date_start: 
                    if date_min > date_start:
                        date_min = date_start
            result[i] = date_min                                  
        return result
    
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
                'date_end':fields.function(_get_date_end, string='End Date', type='date', help='Date end is calculated based on the cost center related to this contract',store=True),
                'date_start':fields.function(_get_date_start,required=True, string='Start Date', type='date', help='Date start is calculated based on the cost center related to this contract',store=True),
                  
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