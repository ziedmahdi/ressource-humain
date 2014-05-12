# -*- coding: utf-8 -*-
from openerp import addons
from openerp import netsvc, tools, pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _


class salary_type(osv.osv):
    
    _name = 'salary.type'
    
    _rec_name = 'label'
    
    _columns = {
                
                'label':fields.char('Libellé', size=64, required=False),
                
                'payment_planif':fields.selection([
                    ('mensuelle','Mensuelle'),
                    ('trimestrielle','Trimestrielle'),
                    ('annuelle','Annuelle')],'Planification de la paie', select=True),
                 
                 'sex':fields.selection([
                     ('homme','Homme'),
                     ('femme','Femme'),
                      ],'Sexe', select=True),
                
                 'code':fields.char('Code', size=64, required=False)    

                    } 
    
 #test seifffff !                 
salary_type()