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

    
    _columns = { 
                'salary': fields.float('Salary',required=True),
                'salary_type_id':fields.many2one('salary.type', 'Salary type', required=True),                 
                
                'work_time_type':fields.selection([
                     ('complete','Complete'),
                     ('partial','Partial'),
                     ],'Working time type', select=True),
                
                'occupation_rate': fields.integer('Occupation rate',required=True),
                'taxed_at_source':fields.boolean('Taxed at source', required=True),
                'cost_center_ids':fields.many2many('cost.center', 'contract_cost_center_rel', 'hr_contract_id', 'cost_center_id', 'Cost centers'),
                #juste pour eviter le problème de contraint not null sur wage 
                'wage': fields.float('Wage', digits=(16,2), required=True, help="Basic Salary of the employee"),  
                }
    
    _defaults = {
                 'wage' : 0
        }
    

    
inherit_hr_contract()  