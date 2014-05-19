# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import re




class inherit_hr(osv.osv):
    
    _name ='hr.employee'
    
    _inherit = 'hr.employee'
    
    _rec_name = 'name'
    
    #function to make sure that the user has typed a correct email address  
    def onchange_email(self, cr,uid,ids, email):
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return True
        else:                    
            raise osv.except_osv(_('Invalid Email'), _('Please enter a valid email address'))
    
    def _check_work_email(self, cr,uid,ids,context=None):
        employees = self.browse(cr,uid,ids,context=context)        
        for employee in employees:        
            email = employee.work_email
            if not email:
                return False
            else: 
                if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
                    return True
                else:
                    return False
        
    def _check_personal_email(self, cr,uid,ids,context=None):
        employees = self.browse(cr,uid,ids,context=context)
        for employee in employees:
            email = employee.personal_email
            if not email:
                return False
            else: 
                if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
                    return True
                else:
                    return False
    #function to make sure that the user has typed a correct phone number
    def onchange_phone(self, cr,uid,ids, phone):
        if not phone:
                return False
        if re.match("^[+]?[0-9\-./_ ]{8,16}$", phone) != None: 
            return True
        else:
            raise osv.except_osv(_('Invalid Phone Number'), _('Please enter a valid phone number'))
                
    def _check_personal_phone(self, cr,uid,ids,context=None):
        employees = self.browse(cr,uid,ids,context=context)
        for employee in employees:
            phone = employee.personal_phone
            if not phone:
                return False
            else: 
                if re.match("^[+]?[0-9\-./_ ]{8,16}$", phone) != None: 
                    return True
                else:
                    return False
                
    def _check_work_phone(self, cr,uid,ids,context=None):
        employees = self.browse(cr,uid,ids,context=context)
        for employee in employees:
            phone = employee.work_phone
            if not phone:
                return False
            else: 
                if re.match("^[+]?[0-9\-./_ ]{8,16}$", phone) != None: 
                    return True
                else:
                    return False
    
    #function to set the matricule field automatically 
    def _get_matricule(self, cr, uid, context=None):            
        sql_req ="""SELECT matricule  
             FROM hr_employee
             ORDER BY matricule DESC
             LIMIT 1"""
        cr.execute(sql_req)
        sql_res = cr.dictfetchone()
        if not sql_res:
            return 1        
        sql_res = int(sql_res['matricule'])                 
        return sql_res  + 1
    
    def _get_employee_status(self, cr, uid, ids, field_name, args, context=None):
        result = {}
        for i in ids:            
            sql_req ="""SELECT count(*) as count_active_contracts  
                 FROM hr_contract
                 WHERE employee_id=%d
                 AND active = TRUE
                 """ % (i,)
            cr.execute(sql_req)
            sql_res = cr.dictfetchone()        
            if sql_res['count_active_contracts'] > 0:
                result[i]=True
            else:
                result[i]=False
        return result
#     def _get_employee_status(self, cr, uid, ids, field_name, args, context=None):
#         result = {}
#         for i in ids:
#             contract = self.browse(cr,uid,i,context=context)
#             date_min= current_date = date.today()            
#             cost_center = contract.cost_center_ids
#             for cost_center_details in cost_center:
#                 date_entry=cost_center_details.date_entry
#                 date_release=cost_center_details.date_release                                    
#                 date_start =datetime.datetime.strptime(date_entry, "%Y-%m-%d").date()
#                 date_end =datetime.datetime.strptime(date_release, "%Y-%m-%d").date()
#                 if date_end >= current_date and current_date >= date_start: 
#                     if date_min > date_start:
#                         date_min = date_start
#             result[i] = date_min                                  
#         return result  
    
    
    _columns = {
        'first_name':fields.char('First Name', size=64, required=True, readonly=False),
        'personal_phone': fields.char('Personal Phone', size=16, readonly=False),
        'personal_email': fields.char('Personal Email', size=64),
        'ssn': fields.char('Security Social Number', size=32),
        'matricule':fields.char('Matricule', size=16, readonly=True ),
        'address': fields.char('Address', size=240),
        'zip': fields.char('Zip', size=32),
        'city': fields.char('City', size=64),
        'country': fields.char('Country', size=64),
        'title':fields.selection([('mr', 'Mr'),('ms', 'Ms'),('miss', 'Miss')], 'Title'),
        'active':fields.function(_get_employee_status, string='Active', type='boolean', help='Employee status is calculated automatically',store=True),
        }
    
    _defaults ={
        'matricule' : _get_matricule
        }
    
    _constraints = [(_check_work_email, 'Invalid Work Email. Please enter a valid email address', ['work_email']),
                    (_check_personal_email, 'Invalid Personal Email. Please enter a valid email address', ['personal_email']),
                    (_check_personal_phone, 'Invalid Personal Phone Number. Please enter a valid phone number', ['personal_phone']),
                    (_check_work_phone, 'Invalid Work Phone Number. Please enter a valid phone number', ['work_phone']),
                    ]

    
inherit_hr() 