#-*- coding: utf-8 -*-
from openerp import addons
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools

class cost_center(osv.osv):
    _name="cost.center"
    _description=" centre de cout"
    _columns = {
              
                'date_entry': fields.date('Date of Entry'), 
                'date_release': fields.date('Realease Date'),
                
                #la fonction de l'employÃ© champs many2one
                'function_id': fields.many2one('function', "Function", required=True),
                'department_id': fields.many2one('hr.department', "Department", required=True),
                'number_of_hours_worked': fields.integer('Number of hours worked'),
                'supervisor':fields.char('Supervisor', size=64, required=True),
                'occupation_rate': fields.integer('Occupation Rate'),
            
                    }
    
#     def _check_dates(self, cr, uid, ids, context=None):
#         for date in self.read(cr, uid, ids, ['date_entry', 'date_release'], context=context):
#             if date['date_release'] and date['date_entry'] and date['date_entry'] > contract['date_release']:
#                 return False
#         return True 
# 
#       
# 
#     _constraints = [
#         (_check_dates, 'Error! Cost Center, date entry must be less than contract date release.', ['date_entry', 'date_release'])
#     ]    
cost_center()
    
    