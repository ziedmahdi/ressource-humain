# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import datetime 
from datetime import date
from openerp.addons.pcd.cost_center import cost_center



#function to check the integrity of occupation rate in each period of the contract
def check_occupation_rate_on_each_period(l):
    max_occupation_rate = {}
    max_occupation_rate['occupation_rate']=0
    for ele in l:
        if ele['occupation_rate'] > max_occupation_rate['occupation_rate']:
            max_occupation_rate ={ 
                                  'occupation_rate' :ele['occupation_rate'],
                                  'date_start' : ele['date_start'],
                                  'date_end' : ele['date_end'],
                                  } 
    return max_occupation_rate

#function to check dates
def check_dates(date_start,date_end):
    if date_start >= date_end:
        raise osv.except_osv(_('Invalid Dates'), _('Entry date must be before release date'))
    
#function to check if occupation rate of the cost center is under 100
def check_cost_center_occupation_rate(occupation_rate): 
    if occupation_rate > 100 or occupation_rate < 0:
        raise osv.except_osv(_('Invalid Occupation Rate'), _('Occupation rate must be between 0 and 100'))

#function to insert a cost center's period into a list of period, with integration of
#occupation rate
#the list have to be not empty 
def insert_cost_center_into_list(date_start, date_end, occupation_rate, l,boolean):
    list_length = len(l)
    #insertion of the entry's date of current cost center  
    i = 0
    not_found = True                    
    while i < list_length and not_found:#0                        
        if l[i]['date_end'] > date_start and date_start >= l[i]['date_start']: #1            
            not_found = False
            if date_end <= l[i]['date_end'] and date_end > l[i]['date_start']:#2
                if date_start == l[i]['date_start']:
                                            
                    if date_end != l[i]['date_end']:
                        l.insert(i+1,{
                                      'occupation_rate' :l[i]['occupation_rate'],
                                      'date_start' : date_end,
                                      'date_end' :l[i]['date_end'],
                                      })
                        l[i]['date_end'] = date_end
                    l[i]['occupation_rate'] += occupation_rate
                    if boolean:
                        if l[i]['occupation_rate']  > 100 :
                            return False
                else:
                    l.insert(i,{
                                  'occupation_rate' :l[i]['occupation_rate'],
                                  'date_start' : l[i]['date_start'],
                                  'date_end' :date_start,
                                  })
                    l[i+1]['occupation_rate'] += occupation_rate
                    if boolean:
                        if l[i+1]['occupation_rate']  > 100 :
                            return False
                    l[i+1]['date_start']=  date_start
                    
                    if date_end != l[i+1]['date_end']:
                        l.insert(i+2,{
                                      'occupation_rate' :l[i]['occupation_rate'],
                                      'date_start' : date_end,
                                      'date_end' : l[i+1]['date_end'],
                                      })
                    l[i+1]['date_end']=  date_end
#                 else:
#                     if i != (len(l)-1):
#                         if date_end > l[i+1]['date_start']:
#                             l.insert(i+1,{
#                                           'occupation_rate' :occupation_rate,
#                                           'date_start' : date_start,
#                                           'date_end' : l[i+1]['date_start'],
#                                           })
#                             k=i+2
#                             not_found_3 = True
#                             while k < len(l) and not_found_3:
#                                 if date_end <= l[k]['date_end']: 
#                                     if date_end > l[k]['date_start']:#5
#                                         not_found_3 = False                            
#                                         if date_end != l[k]['date_end']:
#                                             l.insert(k+1,{
#                                               'occupation_rate' : l[k]['occupation_rate'],
#                                               'date_start' : date_end,
#                                               'date_end' : l[k]['date_end'],
#                                               })        
#                                             l[k]['date_end'] = date_end 
#                                         l[k]['occupation_rate'] += occupation_rate
#                                         if boolean:
#                                             if l[k]['occupation_rate']  > 100 :
#                                                 return False
#                                     else:#5
#                                         l.insert(k,{
#                                           'occupation_rate' : occupation_rate,
#                                           'date_start' : l[k]['date_start'],
#                                           'date_end' : date_end,
#                                           })                                                                                                                                       
#                                 else:
#                                     l[k]['occupation_rate'] += occupation_rate
#                                     if boolean:
#                                         if l[k]['occupation_rate']  > 100 :
#                                             return False
#                                 k+=1
#                             if not_found_3:
#                                 l.append({
#                                           'occupation_rate' : occupation_rate,
#                                           'date_start' : l[len(l)-1]['date_end'],
#                                           'date_end' : date_end,
#                                           })
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
#                         else:
#                             l.append({
#                                       'occupation_rate' :occupation_rate,
#                                       'date_start' : date_start,
#                                       'date_end' : date_end,
#                                       })
#                         
#                     else:
#                         l.append({
#                                   'occupation_rate' :occupation_rate,
#                                   'date_start' : date_start,
#                                   'date_end' : date_end,
#                                   })
            else:#2
                #the date start and date end are not in the same period 
                #we should find the period that date end belong to
                if l[i]['date_start']!=date_start:  
                    l.insert(i+1,{
                              'occupation_rate' :l[i]['occupation_rate']+occupation_rate,
                              'date_start' : date_start,
                              'date_end' : l[i]['date_end'],
                              })
                    l[i]['date_end']=  date_start
                    j = i+2
                else:
                    l[i]['occupation_rate']+=occupation_rate
                    j = i+1
                
                
                not_found_2 = True
                while j < len(l) and not_found_2:
                    if date_end <= l[j]['date_end']: 
                        not_found_2 = False
                        if date_end > l[j]['date_start']:#5                                                        
                            if date_end != l[j]['date_end']:
                                l.insert(j+1,{
                                  'occupation_rate' : l[j]['occupation_rate'],
                                  'date_start' : date_end,
                                  'date_end' : l[j]['date_end'],
                                  })        
                                l[j]['date_end'] = date_end 
                            l[j]['occupation_rate'] += occupation_rate
                            if boolean:
                                if l[j]['occupation_rate']  > 100 :
                                    return False
                        else:#5
                            l.insert(j,{
                              'occupation_rate' : occupation_rate,
                              'date_start' : l[j-1]['date_end'],
                              'date_end' : date_end,
                              })                                                                                                                                       
                    else:
                        l[j]['occupation_rate'] += occupation_rate
                        if boolean:
                            if l[j]['occupation_rate']  > 100 :
                                return False
                    j+=1
                if not_found_2:
                    l.append({
                              'occupation_rate' : occupation_rate,
                              'date_start' : l[len(l)-1]['date_end'],
                              'date_end' : date_end,
                              })
#                     l.insert(i+1,{
#                                   'occupation_rate' :l[i]['occupation_rate']+occupation_rate,
#                                   'date_start' : date_start,
#                                   'date_end' : l[i]['date_end'],
#                                   })
#                     l[i]['date_end']=date_start  

        else:#1
            if i != len(l)-1:
                if date_start >= l[i]['date_end'] and date_start < l[i+1]['date_start']:
                    not_found = False
                    if date_end > l[i+1]['date_start']:
                        l.insert(i+1,{
                                      'occupation_rate' :occupation_rate,
                                      'date_start' : date_start,
                                      'date_end' : l[i+1]['date_start'],
                                      })
                        k=i+2
                        not_found_3 = True
                        while k < len(l) and not_found_3:
                            if date_end <= l[k]['date_end']: 
                                if date_end > l[k]['date_start']:#5
                                    not_found_3 = False                            
                                    if date_end != l[k]['date_end']:
                                        l.insert(k+1,{
                                          'occupation_rate' : l[k]['occupation_rate'],
                                          'date_start' : date_end,
                                          'date_end' : l[k]['date_end'],
                                          })        
                                        l[k]['date_end'] = date_end 
                                    l[k]['occupation_rate'] += occupation_rate
                                    if boolean:
                                        if l[k]['occupation_rate']  > 100 :
                                            return False
                                else:#5
                                    l.insert(k,{
                                      'occupation_rate' : occupation_rate,
                                      'date_start' : l[k]['date_start'],
                                      'date_end' : date_end,
                                      })                                                                                                                                       
                            else:
                                l[k]['occupation_rate'] += occupation_rate
                                if boolean:
                                    if l[k]['occupation_rate']  > 100 :
                                        return False
                            k+=1
                        if not_found_3:
                            l.append({
                                      'occupation_rate' : occupation_rate,
                                      'date_start' : l[len(l)-1]['date_end'],
                                      'date_end' : date_end,
                                      })
#####################################                                                
                        
                    else:
                        l.insert(i+1,{
                                  'occupation_rate' :occupation_rate,
                                  'date_start' : date_start,
                                  'date_end' : date_end,
                                  })
                
                
                    
            
            #we go to the next period
            i+=1         
        
#         else:#1
#             #we go to the next period
#             i+=1
    #0
    if not_found:
    #the start date is little than the start date of the first period                
        if date_start < l[0]['date_start']:#3              
            #it can be either
            #the added period is grater than all the period in the list  
            if date_end > l[len(l)-1]['date_end']:
                for ele in l:
                    ele['occupation_rate'] += occupation_rate
                    if boolean:
                        if ele['occupation_rate']  > 100 :
                            return False
                
                l.insert(0,{
                              'occupation_rate' :occupation_rate,
                              'date_start' : date_start,
                              'date_end' : l[0]['date_start'],
                              })
                l.append({
                          'occupation_rate' :occupation_rate,
                          'date_start' : l[len(l)-1]['date_end'],
                          'date_end' : date_end,
                          })
                
            #the end date is exactly the end date of the last period     
            elif date_end == l[len(l)-1]['date_end']:
                for ele in l:
                    ele['occupation_rate'] += occupation_rate
                    if boolean:
                        if ele['occupation_rate']  > 100 :
                            return False
                
                l.insert(0,{
                              'occupation_rate' :occupation_rate,
                              'date_start' : date_start,
                              'date_end' : l[0]['date_start'],
                              })
                                                                  
            #the added period is before all the periods in the list
            elif date_end < l[0]['date_start']:
                l.insert(0,{
                          'occupation_rate' :occupation_rate,
                          'date_start' : date_start,
                          'date_end' : date_end,
                          })
            #the added period intersect one of the periods in the list                 
            else:
                l.insert(0,{
                          'occupation_rate' :0, #it will be added by the loop
                          'date_start' : date_start,
                          'date_end' : l[0]['date_start'],
                          })
                #we find the end date is situated in which period
                i = 0
                for ele in l:
                    if date_end <= l[i]['date_end'] and date_end > l[i]['date_start']:                        
                        if date_end != l[i]['date_end']:
                            l.insert(i+1,{
                              'occupation_rate' : l[i]['occupation_rate'],
                              'date_start' : date_end,
                              'date_end' : l[i]['date_end'],
                              })        
                            l[i]['date_end'] = date_end
                        l[i]['occupation_rate'] += occupation_rate
                        if boolean:
                            if l[i]['occupation_rate']  > 100 :
                                return False
                        break                                                 
                    else:
                        l[i]['occupation_rate'] += occupation_rate
                        if boolean:
                            if l[i]['occupation_rate']  > 100 :
                                return False
                        i+=1
                
        #the start date is grater than the end date of the last period
        elif date_start >= l[len(l) - 1]['date_end']:
            l.append({
                      'occupation_rate' :occupation_rate,
                      'date_start' : date_start,
                      'date_end' : date_end,
                      })
    return True




class inherit_hr_contract(osv.osv):
    
    _name ='hr.contract' 
    
    _inherit = 'hr.contract'
    
    #function to check if the salary has a correct value
    def onchange_salary(self,cr,uid,ids,salary):
        if str(salary).isdigit():
            return True
        else:    
            raise osv.except_osv(_('Invalid salary'), _('Please enter a valid salary'))

    #function to calculate the occupation rate of a contract
    def _get_contract_occupation_rate(self, cr, uid, ids=[], field_name='occupation_rate', args=None, context=None):
        result = {}
        if not ids:           
            sql_req="""SELECT  id
                    FROM hr_contract""" 
            cr.execute(sql_req)
            sql_res = cr.dictfetchall()
            if not sql_res:
                return result
            else:
                for ele in sql_res:
                    ids.append(ele['id'])
                            
        current_date = date.today()
        for i in ids:        
            contract = self.browse(cr,uid,i,context=context)
            occupation_rate =0
            cost_center = contract.cost_center_ids
            for cost_center_details in cost_center:                                   
                date_start =datetime.datetime.strptime(cost_center_details.date_entry, "%Y-%m-%d").date()
                date_end =datetime.datetime.strptime(cost_center_details.date_release, "%Y-%m-%d").date()
                if date_end >= current_date and current_date >= date_start:            
                    occupation_rate +=   cost_center_details.occupation_rate        
            result[i] =  occupation_rate                                                                                        
        return result
            
            
            
            
    # function to update the occupation rate and verify its integrity                        
    def onchange_cost_center(self,cr,uid,ids,cost_center_change=False,employee_id=False,boolean=False):                    
        occupation_rate = 0
        i=0
        l = []        
        first_creation = False
        current_date = date.today()
        if not ids:
            cost_center = cost_center_change
            first_creation = True
        else:
            if cost_center_change is False:
                first_creation = True
            contract = self.browse(cr,uid,ids[0],None)#we are sure that it's only one contract
            cost_center = contract.cost_center_ids                        
             
        for cost_center_details in cost_center:
            if cost_center_change != False:            
                if cost_center_change[i][2] is False:
                    cost_center_date_entry = cost_center_details.date_entry
                    cost_center_date_release = cost_center_details.date_release
                    cost_center_occupation_rate = cost_center_details.occupation_rate
                    cost_center_supervisor = cost_center_details.supervisor
                else:
                    if 'occupation_rate' in cost_center_change[i][2].keys():
                        cost_center_occupation_rate = cost_center_change[i][2]['occupation_rate']
                    else:
                        cost_center_occupation_rate = cost_center_details.occupation_rate
                    check_cost_center_occupation_rate(cost_center_occupation_rate)
                    if 'supervisor' in cost_center_change[i][2].keys():
                        cost_center_supervisor = cost_center_change[i][2]['supervisor']
                    else:
                        cost_center_supervisor = cost_center_details.supervisor
                    if employee_id != False:
                        self._check_employee_recursion(cr,uid,False,None,False,cost_center_supervisor,employee_id)
                    if 'date_entry' in cost_center_change[i][2].keys():
                        cost_center_date_entry = cost_center_change[i][2]['date_entry']
                    else:
                        cost_center_date_entry = cost_center_details.date_entry                
                    if 'date_release' in cost_center_change[i][2].keys():
                        cost_center_date_release = cost_center_change[i][2]['date_release']
                    else:
                        cost_center_date_release = cost_center_details.date_release
            else:
                cost_center_date_entry = cost_center_details.date_entry
                cost_center_date_release = cost_center_details.date_release
                cost_center_occupation_rate = cost_center_details.occupation_rate
                cost_center_supervisor = cost_center_details.supervisor
            i+=1                
            date_start =datetime.datetime.strptime(cost_center_date_entry, "%Y-%m-%d").date()
            date_end =datetime.datetime.strptime(cost_center_date_release, "%Y-%m-%d").date()
            cost_center_occupation_rate 
            check_dates(date_start,date_end)            
            if l==[]:
                l.append({
                          'occupation_rate' :cost_center_occupation_rate,
                          'date_start' : date_start,
                          'date_end' :date_end,
                 })
            else:
                insert_cost_center_into_list(date_start, date_end, cost_center_occupation_rate, l,False)
            
            if date_end >= current_date and current_date >= date_start:            
                occupation_rate +=   cost_center_occupation_rate             
        
        
        #we add the new cost centers
        if not first_creation:
            list_length = len(cost_center_change)
            while i < list_length:
                cost_center_supervisor = cost_center_change[i][2]['supervisor']
                if employee_id != False:
                    self._check_employee_recursion(cr,uid,False,None,False,cost_center_supervisor,employee_id)
                cost_center_occupation_rate = cost_center_change[i][2]['occupation_rate']
                check_cost_center_occupation_rate(cost_center_occupation_rate)
                cost_center_date_entry = cost_center_change[i][2]['date_entry']
                cost_center_date_release = cost_center_change[i][2]['date_release']
                date_start =datetime.datetime.strptime(cost_center_date_entry, "%Y-%m-%d").date()
                date_end =datetime.datetime.strptime(cost_center_date_release, "%Y-%m-%d").date()
                check_dates(date_start,date_end)                
                if date_end >= current_date and current_date >= date_start:            
                    occupation_rate +=   cost_center_occupation_rate             
                i+=1
                if l==[]:
                    l.append({
                              'occupation_rate' :cost_center_occupation_rate,
                              'date_start' : date_start,
                              'date_end' :date_end,
                     })
                else:
                    insert_cost_center_into_list(date_start, date_end, cost_center_occupation_rate, l,False)
        
        #we check other contracts associated with this employee
        if employee_id != False:
            sql_req="""SELECT  id
                        FROM hr_contract
                        WHERE employee_id = %d                    
                        """ %(employee_id,)
            if ids:
                sql_req += """AND id <>  %d"""%(ids[0],)
            cr.execute(sql_req)
            sql_res = cr.dictfetchall()
            if not sql_res:
                pass
            else:
                other_contracts_ids =[]
                for ele in sql_res:
                    other_contracts_ids.append(ele['id'])
                other_contracts = self.browse(cr,uid,other_contracts_ids,None)
                for other_contract in other_contracts:
                    cost_center = other_contract.cost_center_ids                                
                    for cost_center_details in cost_center:
                        cost_center_date_entry = cost_center_details.date_entry
                        cost_center_date_release = cost_center_details.date_release
                        cost_center_occupation_rate = cost_center_details.occupation_rate
                        date_start =datetime.datetime.strptime(cost_center_date_entry, "%Y-%m-%d").date()
                        date_end =datetime.datetime.strptime(cost_center_date_release, "%Y-%m-%d").date()
                        if l==[]:
                            l.append({
                                      'occupation_rate' :cost_center_occupation_rate,
                                      'date_start' : date_start,
                                      'date_end' :date_end,
                             })
                        else:
                            insert_cost_center_into_list(date_start, date_end, cost_center_occupation_rate, l,False)                    
             
                                
        print(l)
        res={
                'value':{
                         'occupation_rate': occupation_rate,                                 
                         },
             }
        
        max_occupation_rate = check_occupation_rate_on_each_period(l)
        if max_occupation_rate['occupation_rate'] > 100:
            if boolean == True:
                return False            
#            valid_occupation_rate = 100 + last_occupation_rate - max_occupation_rate
            message = """The occupation rate between %s and %s is %d""" %(max_occupation_rate['date_start'].strftime('%d/%m/%Y'),max_occupation_rate['date_end'].strftime('%d/%m/%Y'),max_occupation_rate['occupation_rate']),
            res['warning']={
                            'title': 'Occupation rate is incorrect',
                            'message': message,
                            }
        
        if boolean == True:
            return True
        else:
            return res
            
                    
    #function to check the occupation rate
    #the principle is to create a list witch contains every important period for the employee 
    #associated with this contract    
    def _check_occupation_rate(self, cr,uid,ids,context=None):
        l=[]
        #1st step check the current contract
        contracts = self.browse(cr,uid,ids,context=context)
        for contract in contracts:
            cost_centers = contract.cost_center_ids
            #if the contract is not associated with any cost center, it's valid  
            if not cost_centers:
                return True
            #there is at least one cost center associated with this contract 
            for cost_center in cost_centers:
                #if it's the first cost_center
                date_start = datetime.datetime.strptime(cost_center.date_entry, "%Y-%m-%d").date()
                date_end = datetime.datetime.strptime(cost_center.date_release, "%Y-%m-%d").date()
                if l==[]:
                    l.append({
                              'occupation_rate' :cost_center.occupation_rate,
                              'date_start' : date_start,
                              'date_end' :date_end,
                     })
                else:
                    if not insert_cost_center_into_list(date_start, date_end, cost_center.occupation_rate, l,True):
                        return False
             
            sql_req="""SELECT  id
                    FROM hr_contract                    
                    WHERE employee_id = %d
                    AND id <> %d
                    """ %(contract.employee_id,contract.id,)
            cr.execute(sql_req)
            sql_res = cr.dictfetchall()
            if not sql_res:
                return True
            else:
                others_contract_ids =[]
                for ele in sql_res:
                    others_contract_ids.append(ele['id'])            
                others_contract = self.browse(cr,uid,others_contract_ids,context=context)
                for one_other_contract in others_contract:
                    cost_centers = one_other_contract.cost_center_ids
                    for cost_center in cost_centers:
                        date_start = datetime.datetime.strptime(cost_center.date_entry, "%Y-%m-%d").date()
                        date_end = datetime.datetime.strptime(cost_center.date_release, "%Y-%m-%d").date()
                        if not insert_cost_center_into_list(date_start, date_end, cost_center.occupation_rate, l,True):
                            return False
        return True                    
                            
                                                                                                
    
#     def _check_occupation_rate(self, cr,uid,ids,context=None):        
#         occupation_rate=0
#         contracts = self.browse(cr,uid,ids,context=context)
#         current_date = date.today()
#         for contract in contracts:
#             cost_center = contract.cost_center_ids
#             for cost_center_details in cost_center:                                   
#                 date_start =datetime.datetime.strptime(cost_center_details.date_entry, "%Y-%m-%d").date()
#                 date_end =datetime.datetime.strptime(cost_center_details.date_release, "%Y-%m-%d").date()
#                 if date_end >= current_date and current_date >= date_start:            
#                     occupation_rate +=   cost_center_details.occupation_rate  
#         if occupation_rate > 100:            
#             return False
#         return True
    
    #function to check if we can associated the chosen employee with this contract   
    def onchange_employee_id(self,cr,uid,ids,employee_id,cost_center_change,boolean=False):
    # if not ids and not cost_center_change:
    #       return True
        if self.onchange_cost_center(cr,uid,ids,cost_center_change,employee_id,True):
                return True
        else:
            res={
                    'warning':{
                               'title': 'Cannot associate this contract with the chosen employee',
                               'message': 'The total of occupation rate has exceed 100%',
                               }
                 }
            return res
        
        
        
        
                                                        
#         sql_req="""SELECT occupation_rate
#                    FROM hr_contract
#                    WHERE employee_id = %d                   
#                    """ %(employee_id,)
#         if ids:
#             sql_req += """AND id <>  %d"""%(ids[0],)
#         cr.execute(sql_req)
#         sql_res = cr.dictfetchall()
#         if not sql_res:
#             return True #even if the contract occupation rate is greater than 100%         
#         employee_occupation_rate=occupation_rate
#         for lign in sql_res:
#             if lign['occupation_rate'] is None:
#                 continue
#             else:
#                 employee_occupation_rate += int(lign['occupation_rate'])
#         if employee_occupation_rate > 100:
#             if boolean:
#                 return False
#             else:
#                 res={
#                      'warning':{
#                                 'title': 'Cannot associate this contract with the chosen employee',
#                                 'message': 'The total of occupation rate has exceed 100%',
#                                 }
#                  }            
#                 return res
#         else:
#             return True
    
    def _check_employee_id(self, cr,uid,ids,context=None):
        contract = self.browse(cr,uid,ids[0],context=context)                
        employee_id=contract.employee_id._id
        if self.onchange_employee_id(cr,uid,ids,employee_id,False,True):
            return True
        else:
            return False
    
    
    
    def _get_associated_employee_status(self,cr,employee_id):
        sql_req="""SELECT active
                    FROM hr_employee
                    WHERE id = %d
                    LIMIT 1
                """ %(employee_id,)
        cr.execute(sql_req)
        sql_res = cr.dictfetchone()
        return sql_res['active']
    
    def _set_associated_employee_status(self,cr,employee_id,status):
        sql_req="""UPDATE hr_employee
                    SET active = %r
                    WHERE id= %d""" %(status,employee_id,)
        cr.execute(sql_req)
    
    def _get_if_employee_has_another_active_contract(self,cr,employee_id,contract_id):
        sql_req="""SELECT count(*) as count_contract
                    FROM hr_contract
                    WHERE active = TRUE
                    AND employee_id = %d
                    AND id <> %d
                    """ %(employee_id,contract_id,)
        cr.execute(sql_req)
        sql_res = cr.dictfetchone()
        if sql_res['count_contract'] > 0:
            return True
        else:
            return False
        
        
        
        
            
            
    #function to tell if a contract is active or not  
    def _get_contract_status(self, cr, uid, ids=[], field_name='Status', args=None, context=None):
        result = {}        
        current_date = date.today()
        if not ids:           
            sql_req="""SELECT  id
                    FROM hr_contract""" 
            cr.execute(sql_req)
            sql_res = cr.dictfetchall()
            if not sql_res:
                return result
            else:
                for ele in sql_res:
                    ids.append(ele['id'])
        for i in ids:
            result[i]=False            
            contract = self.browse(cr,uid,i,context=context)            
            contract_id = int (contract.id)
            employee_id = contract.employee_id            
            cost_center = contract.cost_center_ids
            if not cost_center:                
                if not self._get_if_employee_has_another_active_contract(cr,employee_id,contract_id):
                    self._set_associated_employee_status(cr,employee_id,False)
                else:
                    self._set_associated_employee_status(cr,employee_id,True)
                continue
            for cost_center_details in cost_center:
                date_entry=cost_center_details.date_entry
                date_release=cost_center_details.date_release                                    
                date_start =datetime.datetime.strptime(date_entry, "%Y-%m-%d").date()
                date_end =datetime.datetime.strptime(date_release, "%Y-%m-%d").date()
                if date_end >= current_date and current_date >= date_start:                     
                    result[i]=True                    
                    #activate the associated employee (if is not already)
                    if not self._get_associated_employee_status(cr,employee_id):
                        self._set_associated_employee_status(cr,employee_id,True)
                    break                                 
            if result[i]==False:
                if not self._get_if_employee_has_another_active_contract(cr,employee_id,contract_id):
                    self._set_associated_employee_status(cr,employee_id,False)
                else:
                    self._set_associated_employee_status(cr,employee_id,True)                                                           
        return result
    
    def _get_date_end(self, cr, uid, ids, field_name, args, context=None):
        result = {}
        for i in ids:
            date_max = False
            contract = self.browse(cr,uid,i,context=context)                         
            cost_center = contract.cost_center_ids
            if not cost_center:
                result[i] = date.today()
                continue
            for cost_center_details in cost_center:               
                date_release=cost_center_details.date_release                                                   
                date_end =datetime.datetime.strptime(date_release, "%Y-%m-%d").date()
                if date_max is False:
                    date_max = date_end                 
                if date_max < date_end:
                    date_max = date_end
            result[i] = date_max                                  
        return result
    
    def _get_date_start(self, cr, uid, ids, field_name, args, context=None):
        result = {}
        for i in ids:
            date_min = False
            contract = self.browse(cr,uid,i,context=context)                        
            cost_center = contract.cost_center_ids
            if not cost_center:
                result[i] = date.today()
                continue
            for cost_center_details in cost_center:
                date_entry=cost_center_details.date_entry                                                
                date_start =datetime.datetime.strptime(date_entry, "%Y-%m-%d").date()
                if date_min is False:
                    date_min = date_start                
                if date_min > date_start:
                    date_min = date_start
            result[i] = date_min                                  
        return result
    
    def _check_employee_recursion(self, cr,uid,ids=False,context=None,boolean=True,supervisor_id=False,employee_id=False):    
            if boolean == False:
                if supervisor_id == employee_id:
                    raise osv.except_osv(_('Employee can\'t be his own boss'),_('Can not associate contract with this employee '))
            else:                
                contract = self.browse(cr,uid,ids[0],context=context)        
                cost_center = contract.cost_center_ids                    
                for cost_center_details in cost_center:
                    supervisor_id = cost_center_details.supervisor
                    employee_id = contract.employee_id
                    if supervisor_id == employee_id:
                        return False
                return True 
        
    def action_draft(self,cr,uid,ids,context=None):
        #set to "draft" state
        return self.write(cr,uid,ids,{'state':'draft'},context=context)
    
    def action_ongoing(self,cr,uid,ids,context=None):
        #set to "ongoing" state
        return self.write(cr,uid,ids,{'state':'ongoing'},context=context)
    
    def action_done(self,cr,uid,ids,context=None):
        #set to "done" state
        return self.write(cr,uid,ids,{'state':'done'},context=context)
  
                    
                
                
            
        
    
    _columns = { 
                'salary': fields.float('Salary',required=True),
                'salary_type_id':fields.many2one('salary.type', 'Salary type', required=True,ondelete="cascade"),                 
                'employee_id': fields.many2one('hr.employee', "Employee", required=True,ondelete="cascade",domain="['|', ('active', '=',True), ('active', '=',False)]"),
                'work_time_type':fields.selection([
                     ('complete','Complete'),
                     ('partial','Partial'),
                     ],'Working time type', select=True),
                'active': fields.function(_get_contract_status, string='Active', type='boolean', help='Contract status is calculated automatically',readonly=True,store=True),
                'occupation_rate': fields.function(_get_contract_occupation_rate, string='Occupation rate', type='integer', help='Occupation rate calculated based on the cost center related to this contract',readonly=True,store=True),
                'taxed_at_source':fields.boolean('Taxed at source', required=False),
                'cost_center_ids': fields.one2many('cost.center', 'contract_id', 'Cost centers'),                
                'date_end':fields.function(_get_date_end, string='End Date', type='date', help='Date end is calculated based on the cost center related to this contract',store=True),
                'date_start':fields.function(_get_date_start,required=True, string='Start Date', type='date', help='Date start is calculated based on the cost center related to this contract',store=True),
                'state':fields.selection([('draft','Draft'),('ongoing','Ongoing'),('done','Done')],'Status',readonly=True,required=True),

                  
    }            
    
    _defaults = {
                 'wage':0,
                 'active': 0,
                 'state':'draft'

        }
    
    _constraints = [
                    (_check_occupation_rate, 'The occupation rate has exceed 100% Please check the associated cost center', ['occupation_rate']),
                    (_check_employee_id, 'Cannot associate this contract with the chosen employee', ['employee_id']),
                    (_check_employee_recursion, 'Employee can\'t be his own boss', ['employee_id'])
                ]
    

    
inherit_hr_contract()  