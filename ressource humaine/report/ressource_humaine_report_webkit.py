from openerp.report import report_sxw
 
class ressource_humaine_report_webkit(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(ressource_humaine_report_webkit, self).__init__(cr, uid, name, context=context)
        report_sxw.report_sxw('hr.contract.rep.webkit',
                                  'hr.contract',
                                  'pcd/report/module_rep_webkit.mako',
                                   parser= ressource_humaine_report_webkit)
