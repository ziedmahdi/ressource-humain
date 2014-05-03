# -*- coding: utf-8 -*-
from openerp import addons
from openerp import netsvc, tools, pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _
import re

class inherit_hr(osv.osv):
    
    _name ='hr.employee'
    
    _inherit = 'hr.employee'
    
    def onchange_email(self, cr, uid, ids, email):
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return True
        else:
            raise osv.except_osv(_('Invalid Email'), _('Please enter a valid email address'))
    
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
    
inherit_hr() 