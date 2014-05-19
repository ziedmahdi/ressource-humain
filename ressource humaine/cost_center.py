#-*- coding: utf-8 -*-

from openerp.osv import fields, osv



class cost_center(osv.osv):
    _name="cost.center"
    _description=" centre de cout"
    
    
    #function to make sure that the occupation rate between 1 and 100    
    def _check_occupation_rate(self, cr,uid,ids,context=None):
        employees = self.browse(cr,uid,ids,context=context)
        for employee in employees:
            occupation_rate = employee.occupation_rate
            if not occupation_rate:
                return False
            else:
                if occupation_rate >= 0 and occupation_rate < 101:

                    return True
                else:
                    return False
    

#function to verify that end day bigger than start day    
    def _check_dates(self, cr, uid, ids, context=None):
        
        for date in self.read(cr, uid, ids, ['date_entry', 'date_release'], context=context):
            if date['date_release'] and date['date_entry'] and date['date_entry'] > date['date_release']:
                return False
            return True
         
    
    _columns = {
              
                'date_entry': fields.date('Date of Entry',required=True), 
                'date_release': fields.date('Realease Date',required=True),
                
                #la fonction de l'employee champs many2one
                'function_id': fields.many2one('function', "Function", required=True,ondelete="cascade"),
                'department_id': fields.many2one('hr.department', "Department", required=True,ondelete="cascade"),
                'number_of_hours_worked': fields.integer('Number of hours worked'),
                'supervisor':fields.many2one('hr.employee','Supervisor', required=True,ondelete="cascade"),
                'occupation_rate': fields.integer('Occupation Rate'),
                'contract_id':fields.many2one('hr.contract', 'Contracts'), 
                   }
    
    
    _constraints = [(_check_dates, 'Error! Cost Center, date entry must be less than contract date release.', ['date_entry', 'date_release']),
                    (_check_occupation_rate, 'Error! The cost center occupation rate must be between 0 and 100', ['occupation_rate']),
         ]    
    
    
    
   

           
      

            
cost_center()
    
    