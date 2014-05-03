# -*- coding: utf-8 -*-
from openerp import addons
from openerp import netsvc, tools, pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _
import re

class inherit_hr(osv.osv):
    
    _name ='hr.employee'
    
    _inherit = 'hr.employee'
    
    #function to make sure that the user has typed a correct email address  
    def onchange_email(self, email):
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return True
        else:                    
            raise osv.except_osv(_('Invalid Email'), _('Please enter a valid email address'))
    
#     def _check_email(self, cr,uid,ids,context=None):
#         employee = self.browse(cr,uid,ids,context=context)
#         self.onchange_email(self, employee.work_email,True)
        
    
    _columns = {
        'first_name':fields.char('First Name', size=64, required=True, readonly=False),
        'personel_phone': fields.char('Personel Phone', size=32, readonly=False),
        'personel_email': fields.char('Personel Email', size=240),
        'ssn': fields.char('Security Social Number', size=32),
        'address': fields.char('Address', size=240),
        'zip': fields.char('Zip', size=32),
        'city': fields.char('City', size=64),
        'country': fields.char('Country', size=64),
        'job': fields.char('Job', size=64)
        }
    
#    _constraints = [(_check_email, 'Please avoid spam in ideas !', ['work_email'])]
    
inherit_hr() 