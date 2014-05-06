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
                'salary_type':fields.char('Type de salaire', required=True),
                'date_start': fields.date('Date début',required=True), 
                'date_end': fields.date('Date fin',required=True),
                'work_time_type':fields.char('Type de temps de travail',required=True), 
                'occupation_time': fields.integer('Taux d\'occupation',required=True),
                'taxed_at_source':fields.char('Imposé à la source', required=True)
                }
    

    
inherit_hr_contract() 