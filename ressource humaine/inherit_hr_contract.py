# -*- coding: utf-8 -*-
from openerp import addons
from openerp import netsvc, tools, pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _
import re
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
           
    #fonction qui vérifie la saisie du salaire après un click sur (Enregistrer)       
    def _check_salary(self, cr,uid,ids,context=None):
        contracts = self.browse(cr,uid,ids,context=context)
        for contract in contracts:
            salaire = contract.salary
            if not salaire:
                return False
            else:
                if salaire.isdigit():
                    return True
                
                
     #reste à implementer vu la relation avec le centre de cout              
    '''def _check_occupation_rate(self, cr,uid,ids,context=None):
        contracts = self.browse(cr,uid,ids,context=context)
        for contract in contracts:
            ocr = contract.occupation_rate
            if not ocr:
                return False
            else: 
                if 
                else:
                        return False  '''             
    
    _columns = { 
                'salary': fields.char('Salary'),
                'salary_type_id':fields.many2one('salary.type', 'Salary type', required=True),                 
                
                'work_time_type':fields.selection([
                     ('complete','Complete'),
                     ('partial','Partial'),
                     ],'Working time type', select=True),
                
                'occupation_rate': fields.integer('Occupation rate'),
                'taxed_at_source':fields.boolean('Taxed at source'),
                'cost_center_ids':fields.many2many('cost.center', 'contract_cost_center_rel', 'hr_contract_id', 'cost_center_id', 'Cost centers'),  
    
                }
    
    _constraints = [(_check_salary, 'Invalid salary. Please enter a valid salary', ['salary'])]

    
inherit_hr_contract()  