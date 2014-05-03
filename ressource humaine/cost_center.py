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
                
                #la fonction de l'employ� je pense qu'il faut relier a HR.JOB
                'function':fields.char('Function', size=64, required=True),
                
                #Un employ� peut travailler en m�me temps dans 1 � n centres de co�ts.
                'employee_id': fields.many2one('hr.employee', "Employee", required=True),
                'department_id': fields.related('employee_id','department_id', type='many2one', relation='hr.department', string="Department", readonly=True),
                'number_of_hours_worked': fields.integer('Number of hours worked'),
                'Departement_head':fields.char('Departement Head', size=64, required=True),

            
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
    
    