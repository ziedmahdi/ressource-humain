# -*- coding: utf-8 -*-

import openerp
from openerp import netsvc, tools, pooler
from openerp.osv import fields, osv

class inherit_hr(osv.osv):
    
    _name ='hr.employee'
    
    _inherit = 'hr.employee'
    
    _columns = {
        'first_name':fields.char('First Name', size=64, required=True, readonly=False),
        }
    
inherit_hr() 