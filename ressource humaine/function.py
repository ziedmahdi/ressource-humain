#-*- coding: utf-8 -*-
from openerp.osv import fields, osv




class function(osv.osv):
    _name="function"
    _description=" fonction "
    _rec_name = "function"
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