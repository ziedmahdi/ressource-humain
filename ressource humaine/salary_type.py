# -*- coding: utf-8 -*-
from openerp.osv import fields, osv



class salary_type(osv.osv):
    
    _name = 'salary.type'
    
    _rec_name = 'label'
    
    _columns = {
                
                'label':fields.char('Label', size=64, required=False),
                
                'payment_planif':fields.selection([
                    ('Monthly','Monthly'),
                    ('Quarterly','Quarterly'),
                    ('Yearly','Yearly')],'Payement planification', select=True),
                 
                 'sex':fields.selection([
                     ('Male','Male'),
                     ('Female','Female'),
                      ],'Sexe', select=True),
                
                 'code':fields.char('Code', size=64, required=False)    

                    } 
                 
salary_type()