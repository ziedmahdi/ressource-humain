# -*- coding: utf-8 -*-
from openerp import addons
from openerp import netsvc, tools, pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _


class inherit_hr_contract(osv.osv):
    
    _name ='hr.contract' 
    
    _inherit = 'hr.contract'
    
    #fonction qui vérifie la saisie du salaire lors d'un click (Onchange)
    def onchange_salary(self,cr,uid,ids,salary):
        if str(salary).isdigit():
            return True
        else:    
            raise osv.except_osv(_('Invalid salary'), _('Please enter a valid salary'))

    #function which calculat the occupation rate for a contract
    def _get_contract_occupation_rate(self, cr, uid, ids, field_name, args, context=None):
        result = {}
        for i in ids:
            
            sql_req =""" SELECT occupation_rate AS occupation_rate
                         FROM cost_center,contract_cost_center_rel
                         WHERE (contract_cost_center_rel.hr_contract_id=%d)
                         AND (contract_cost_center_rel.cost_center_id=cost_center.id)
                         
                         """ % (i,)
#                      AND cost_center.active = TRUE
            cr.execute(sql_req)
            sql_res = cr.dictfetchall()
            result[i]=0
            if sql_res:                
                for lign in sql_res:
                    result[i] += lign['occupation_rate']                 
        return result           
        
    
    _columns = { 
                'salary': fields.float('Salary',required=True),
                'salary_type_id':fields.many2one('salary.type', 'Salary type', required=True),                 
                
                'work_time_type':fields.selection([
                     ('complete','Complete'),
                     ('partial','Partial'),
                     ],'Working time type', select=True),
                
                'occupation_rate': fields.function(_get_contract_occupation_rate, string='Occupation rate', type='integer', help='Occupation rate calculated based on the cost center related to this contract',readonly=True),
                'taxed_at_source':fields.boolean('Taxed at source', required=True),
                'cost_center_ids':fields.many2many('cost.center', 'contract_cost_center_rel', 'hr_contract_id', 'cost_center_id', 'Cost centers'),
                #juste pour eviter le problème de contraint not null sur wage 
                'wage': fields.float('Wage', digits=(16,2), required=True, help="Basic Salary of the employee"),  
                }
    
    _defaults = {
                 'wage' : 0
        }
    

    
inherit_hr_contract()  