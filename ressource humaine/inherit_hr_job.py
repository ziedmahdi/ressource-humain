# -*- coding: utf-8 -*-
from openerp.osv import osv ,fields

class inherit_hr_job(osv.osv):
    
    _name="hr.job"
    
    _inherit="hr.job"
    
    _rec_name = 'name' 
    
    
    _columns = {
            'job_location':fields.char('Job location', size=64, required=True),
                    }
    
    
    
inherit_hr_job()     