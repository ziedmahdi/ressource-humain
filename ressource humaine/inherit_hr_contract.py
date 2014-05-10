# -*- coding: utf-8 -*-
from openerp import addons
from openerp import netsvc, tools, pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _
import datetime

class inherit_hr_contract(osv.osv):
    
    _name ='hr.contract'
    
    _inherit = 'hr.contract'
    
    #function to make sure that the user enter valid start and end dates
    def _check_dates(self, cr,uid,ids,context=None):
        contracts = self.browse(cr,uid,ids,context=context)
        for contract in contracts:
            date_start = contract.date_start
            if not date_start:
                return False            
            else:
                date_start = datetime.strptime(date_start,"%d/%m/%Y")
            date_end = contract.date_end
            if not date_end:
                return False
            else:
                date_end = datetime.strptime(date_end,"%d/%m/%Y") 
            
            if date_end > date_start:
                return True
            else:
                return False
            
    
    _columns = {
                'salary': fields.integer('Salaire',required=True),
                'salary_type_id':fields.many2one('salary.type', 'Type de salaire', required=True), 
                
                
                'work_time_type':fields.selection([
                     ('complet','Complet'),
                     ('partiel','Partiel'),
                     ],'Type de temps de travail', select=True),
                
                'occupation_rate': fields.integer('Occupation rate'),
                'taxed_at_source':fields.boolean('Tax at source' ), 
                }
    
    _constraints = [(_check_dates, 'The date ...............', ['date_start','date_end'])] #to change
    

    
inherit_hr_contract()  