# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _

 

class inherit_hr_job(osv.osv):
    
    _name="hr.job"
    
    _inherit="hr.job"
    
    _rec_name = 'name' 
    
    
    
inherit_hr_job()     