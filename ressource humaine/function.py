#-*- coding: utf-8 -*-
from openerp import addons
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools


class function(osv.osv):
    _name="function"
    _description=" fonction "
    _columns = {
                'function':fields.char('Function', size=64, required=True),
                'state':fields.selection([
                    ('employee','Employee'),
                    ('senior manager','Senior Manager'),
                    ('manager',' Manager'),
                    ('apprentices','Apprentices'),
                    ('trainee','Trainee'),
                     ],    'State' ),
            
                    }
    
function()