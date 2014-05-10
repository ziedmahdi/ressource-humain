#-*- coding: utf-8 -*-
from openerp import addons
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools


class function(osv.osv):
    _name="cost.center.function"
    _description=" fonction "
    _columns = {
                'function':fields.char('Function', size=64, required=True),
                'statut':fields.selection([
                    ('employee','Employee'),
                    ('senior manager','Senior Manager'),
                    ('manager',' Manager'),
                    ('apprentices','Apprentices'),
                    ('trainee','Trainee'),
                     ],    'State', select=True, readonly=True),
            
                    }
    
function()