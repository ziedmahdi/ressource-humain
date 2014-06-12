# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import datetime 
from datetime import date
from openerp.addons.pcd.cost_center import cost_center





class inherit_hr_contract(osv.osv):
    
    _name ='hr.contract' 
    
    _inherit = 'hr.contract'
    
    #fonction qui vérifie la saisie du salaire lors d'un click (Onchange)
    def onchange_salary(self,cr,uid,ids,salary):
        if str(salary).isdigit():
            return True
        else:    
            raise osv.except_osv(_('Invalid salary'), _('Please enter a valid salary'))

    #function to calculate the occupation rate of a contract
    def _get_contract_occupation_rate(self, cr, uid, ids, field_name, args, context=None):
        result = {}                
        current_date = date.today()
        for i in ids:        
            contract = self.browse(cr,uid,i,context=context)
            occupation_rate =0
            cost_center = contract.cost_center_ids
            for cost_center_details in cost_center:                                   
                date_start =datetime.datetime.strptime(cost_center_details.date_entry, "%Y-%m-%d").date()
                date_end =datetime.datetime.strptime(cost_center_details.date_release, "%Y-%m-%d").date()
                if date_end >= current_date and current_date >= date_start:            
                    occupation_rate +=   cost_center_details.occupation_rate        
            result[i] =  occupation_rate                                                                                        
        return result
            
    # function to update the occupation rate and verify its integrity 
    def onchange_cost_center(self,cr,uid,ids,cost_center_change):                    
        occupation_rate = 0
        i=0        
        current_date = date.today()
        if not ids:
            cost_center = cost_center_change
        else:
            contract = self.browse(cr,uid,ids[0],None)#we are sure that it's only one contract
            cost_center = contract.cost_center_ids
            
        for cost_center_details in cost_center:            
            if cost_center_change[i][2] is False:
                cost_center_date_entry = cost_center_details.date_entry
                cost_center_date_release = cost_center_details.date_release
                cost_center_occupation_rate = cost_center_details.occupation_rate
            else:
                if 'occupation_rate' in cost_center_change[i][2].keys():
                    cost_center_occupation_rate = cost_center_change[i][2]['occupation_rate']
                else:
                    cost_center_occupation_rate = cost_center_details.occupation_rate
                
                if 'date_entry' in cost_center_change[i][2].keys():
                    cost_center_date_entry = cost_center_change[i][2]['date_entry']
                else:
                    cost_center_date_entry = cost_center_details.date_entry
                
                if 'date_release' in cost_center_change[i][2].keys():
                    cost_center_date_release = cost_center_change[i][2]['date_release']
                else:
                    cost_center_date_release = cost_center_details.date_release
            i+=1                
            date_start =datetime.datetime.strptime(cost_center_date_entry, "%Y-%m-%d").date()
            date_end =datetime.datetime.strptime(cost_center_date_release, "%Y-%m-%d").date()
            if date_end >= current_date and current_date >= date_start:            
                occupation_rate +=   cost_center_occupation_rate             
                     
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
    
    #function to check the occupation rate
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
    
    #function to 
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
    
    
    
    def _get_associated_employee_status(self,cr,employee_id):
        sql_req="""SELECT active
                    FROM hr_employee
                    WHERE id = %d
                    LIMIT 1
                """ %(employee_id,)
        cr.execute(sql_req)
        sql_res = cr.dictfetchone()
        return sql_res['active']
    
    def _set_associated_employee_status(self,cr,employee_id,status):
        sql_req="""UPDATE hr_employee
                    SET active = %r
                    WHERE id= %d""" %(status,employee_id,)
        cr.execute(sql_req)
    
    def _get_if_employee_has_another_active_contract(self,cr,employee_id,contract_id):
        sql_req="""SELECT count(*) as count_contract
                    FROM hr_contract
                    WHERE active = TRUE
                    AND employee_id = %d
                    AND id <> %d
                    """ %(employee_id,contract_id,)
        cr.execute(sql_req)
        sql_res = cr.dictfetchone()
        if sql_res['count_contract'] > 0:
            return True
        else:
            return False
        
        
        
        
            
            
    #function to tell if a contract is active or not  
    def _get_contract_status(self, cr, uid, ids, field_name, args, context=None):
        result = {}        
        current_date = date.today()
        for i in ids:
            result[i]=False            
            contract = self.browse(cr,uid,i,context=context)            
            contract_id = int (contract.id)
            employee_id = contract.employee_id            
            cost_center = contract.cost_center_ids
            if not cost_center:                
                if not self._get_if_employee_has_another_active_contract(cr,employee_id,contract_id):
                    self._set_associated_employee_status(cr,employee_id,False)
                else:
                    self._set_associated_employee_status(cr,employee_id,True)
                continue
            for cost_center_details in cost_center:
                date_entry=cost_center_details.date_entry
                date_release=cost_center_details.date_release                                    
                date_start =datetime.datetime.strptime(date_entry, "%Y-%m-%d").date()
                date_end =datetime.datetime.strptime(date_release, "%Y-%m-%d").date()
                if date_end >= current_date and current_date >= date_start:                     
                    result[i]=True                    
                    #activate the associated employee (if is not already)
                    if not self._get_associated_employee_status(cr,employee_id):
                        self._set_associated_employee_status(cr,employee_id,True)
                    break                                 
            if result[i]==False:
                if not self._get_if_employee_has_another_active_contract(cr,employee_id,contract_id):
                    self._set_associated_employee_status(cr,employee_id,False)
                else:
                    self._set_associated_employee_status(cr,employee_id,True)                                                           
        return result
    
    def _get_date_end(self, cr, uid, ids, field_name, args, context=None):
        result = {}
        for i in ids:
            date_max = False
            contract = self.browse(cr,uid,i,context=context)                         
            cost_center = contract.cost_center_ids
            if not cost_center:
                result[i] = date.today()
                continue
            for cost_center_details in cost_center:               
                date_release=cost_center_details.date_release                                                   
                date_end =datetime.datetime.strptime(date_release, "%Y-%m-%d").date()
                if date_max is False:
                    date_max = date_end                 
                if date_max < date_end:
                    date_max = date_end
            result[i] = date_max                                  
        return result
    
    def _get_date_start(self, cr, uid, ids, field_name, args, context=None):
        result = {}
        for i in ids:
            date_min = False
            contract = self.browse(cr,uid,i,context=context)                        
            cost_center = contract.cost_center_ids
            if not cost_center:
                result[i] = date.today()
                continue
            for cost_center_details in cost_center:
                date_entry=cost_center_details.date_entry                                                
                date_start =datetime.datetime.strptime(date_entry, "%Y-%m-%d").date()
                if date_min is False:
                    date_min = date_start                
                if date_min > date_start:
                    date_min = date_start
            result[i] = date_min                                  
        return result
    
    def _check_employee_recursion(self, cr,uid,ids,context=None):
        contracts = self.browse(cr,uid,ids,context=context)
        for contract in contracts:
            cost_center = contract.cost_center_ids
            for cost_center_details in cost_center:
                supervisor_id = cost_center_details.supervisor
                employee_id = contract.employee_id
                if supervisor_id == employee_id:
                    return False
            return True 
        
    def action_draft(self,cr,uid,ids,context=None):
        #set to "draft" state
        return self.write(cr,uid,ids,{'state':'draft'},context=context)
    
    def action_confirm(self,cr,uid,ids,context=None):
        #set to "confirmed" state
        return self.write(cr,uid,ids,{'state':'confirmed'},context=context)
    
    def action_done(self,cr,uid,ids,context=None):
        #set to "done" state
        return self.write(cr,uid,ids,{'state':'done'},context=context)
  
                    
                
                
            
        
    
    _columns = { 
                'salary': fields.float('Salary',required=True),
                'salary_type_id':fields.many2one('salary.type', 'Salary type', required=True,ondelete="cascade"),                 
                'employee_id': fields.many2one('hr.employee', "Employee", required=True,ondelete="cascade",domain="['|', ('active', '=',True), ('active', '=',False)]"),
                'work_time_type':fields.selection([
                     ('complete','Complete'),
                     ('partial','Partial'),
                     ],'Working time type', select=True),
                'active': fields.function(_get_contract_status, string='Active', type='boolean', help='Contract status is calculated automatically',readonly=True,store=True),
                'occupation_rate': fields.function(_get_contract_occupation_rate, string='Occupation rate', type='integer', help='Occupation rate calculated based on the cost center related to this contract',readonly=True,store=True),
                'taxed_at_source':fields.boolean('Taxed at source', required=False),
                'cost_center_ids': fields.one2many('cost.center', 'contract_id', 'Cost centers'),                
                'date_end':fields.function(_get_date_end, string='End Date', type='date', help='Date end is calculated based on the cost center related to this contract',store=True),
                'date_start':fields.function(_get_date_start,required=True, string='Start Date', type='date', help='Date start is calculated based on the cost center related to this contract',store=True),
                'state':fields.selection([('draft','Draft'),('confirmed','Confirmed'),('done','Done')],'Status',readonly=True,required=True),

                  
    }            
    
    _defaults = {
                 'wage':0,
                 'active': 0,
                 'state':'draft'

        }
    
    _constraints = [
                    (_check_occupation_rate, 'The occupation rate has exceed 100% Please check the associated cost center', ['occupation_rate']),
                    (_check_employee_id, 'Cannot associate this contract with the chosen employee', ['employee_id']),
                    (_check_employee_recursion, 'Employee can\'t be his own boss', ['employee_id'])
                ]
    

    
inherit_hr_contract()  