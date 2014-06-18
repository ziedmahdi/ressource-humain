# -*- coding: utf-8 -*-
{
    "name": "Human Resource Management",
    "version": "1.0",
    'category': 'Human Resources',
    "depends": ["base","hr","hr_contract","report_webkit"],
    "author": "Feki Zied,Hammami Seifeddine,Trabelsi Zeineb",
    "description": """The object of the present application is to centralize information and to homogenize
procedures for managing human resources.
This application will focus on three complementary aspects:
Monitoring and managing employees,
Monitoring and management of contracts and cost centers,and 
Management of reports""",
    "init_xml": [],
    'update_xml': ["inherit_hr.xml",
		   "cost_center.xml",
	           "inherit_hr_contract.xml",
	           "function.xml",
	           "salary_type_view.xml",
	           "inherit_hr_job.xml",
	           "report/ressource_humaine_report_webkit.xml"],
    'demo_xml': [],
    'installable': True,
    'active': False,
} 
