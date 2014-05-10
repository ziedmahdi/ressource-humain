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
                'salary': fields.integer('Salaire',required=True),
                'salary_type_id':fields.many2one('salary.type', 'Type de salaire', required=True), 
                'date_start': fields.date('Date début',required=True), 
                'date_end': fields.date('Date fin',required=True),
                
                'work_time_type':fields.selection([
                     ('complet','Complet'),
                     ('partiel','Partiel'),
                     ],'Type de temps de travail', select=True),
                
                'occupation_rate': fields.integer('Taux d\'occupation',required=True),
                'taxed_at_source':fields.boolean('Imposé à la source', required=True), 
                }
    

    
inherit_hr_contract()  