# -*- coding: utf-8 -*-
from openerp import addons
from openerp import netsvc, tools, pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time

class inherit_hr_contract(osv.osv):
    
    _name ='hr.contract' 
    
    _inherit = 'hr.contract'  
    
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
                }
    

    
inherit_hr_contract()  