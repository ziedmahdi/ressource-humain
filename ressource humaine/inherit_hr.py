# -*- coding: utf-8 -*-
from openerp import addons
from openerp import netsvc, tools, pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _

class inherit_hr(osv.osv):
    
    _name ='hr.employee'
    
    _inherit = 'hr.employee'
    
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