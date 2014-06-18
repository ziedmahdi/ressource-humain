<html>
	<head>
		<style>
		</style>
	</head>
	
<body>

<%!
    
    import datetime
%>

<%
    
    def getDate():
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
%>

%for obj in objects:
    %for cc in obj.cost_center_ids:
	<table width=100% border="0">
	<tr>
	<td float="right"><img src="http://www.brandsoftheworld.com/sites/default/files/styles/logo-thumbnail/public/112011/openerp.png" alt="logo" align="left" /></td>
        <td valign="Bottom"><h2>Contrat de travail<h2></td>
	<td float="left">${getDate()}</td>
	</tr>
	</table>
	<table width=100% border="0">
  <tr>
    <td ><p>Entre l'employeur(nom et adresse)</p></td>
    <td colspan="5" style="border:1px solid black">${ cc.supervisor.name or ''} ${ cc.supervisor.first_name or ''}, ${ cc.supervisor.address or ''} ${ cc.supervisor.zip or ''} ${ cc.supervisor.city or ''} ${ cc.supervisor.country or ''}</td>
  </tr>
  <tr>
    <td ><p>et le travailleur(nom et adresse)</p></td>
    <td colspan="5" style="border:1px solid black">${ obj.employee_id.name or ''} ${ obj.employee_id.first_name or ''}, ${ obj.employee_id.address or ''} ${ obj.employee_id.zip or ''} ${ obj.employee_id.city or ''} ${ obj.employee_id.country or ''} </td>
  </tr>
  <tr>
    <td>Date de naissance</td>
    <td  style="border:1px solid black">${ obj.employee_id.birthday or ''}</td>
    <td>Sexe</td>
    <td  style="border:1px solid black">${ obj.employee_id.gender or ''}</td>
    <td>Nationalit&eacute;</td>
    <td  style="border:1px solid black">${ obj.employee_id.country_id.name or ''}</td>
  </tr>
  <tr>
    <td>Etat civil</td>
    <td style="border:1px solid black">${ obj.employee_id.marital or ''}</td>
    <td>Nombre d'enfants</td>
    <td style="border:1px solid black">${ obj.employee_id.children or ''}</td>
    <td>Profession</td>
    <td style="border:1px solid black">${ obj.employee_id.job_id.name or ''}</td>
  </tr>
<tr >
    <td colspan="6">Est conclu, sous r&eacute;serve de l'obtention d'une autorisation de s&eacute;jour ou frontali&egrave;re, le contrat de travail suivant :</td>
  </tr>
  <tr>
    <td colspan="6">Convention collective de travail/ contrat-type de travail/ autres</td>
  </tr>
  <tr>
    <td colspan="6" style="border:1px solid black"></td>
  </tr>
  <tr>
    <td colspan="6">Toutes les clauses de l'accord ci-dessus font partie int&eacute;grante du pr&eacute;sent contrat de travail. En cas de divergence entre le contratet l'accord, c'est l'accord qui s'applique.Toute modification ult&eacute;rieure de l'accord est automatiquement adapt&eacute;e au rapport de travail.</td>
  </tr>
  <tr>
    <td colspan="6">L'employ&eacute; est engag&eacute;(e) </td>
  </tr>
  <tr>
    <td colspan="6" style="border:1px solid black">${ obj.work_time_type or ''}</td>
  </tr>
  <tr>
    <td colspan="6" >Lieu de travail</td>
  </tr>
  <tr>
    <td colspan="6" style="border:1px solid black">${ obj.employee_id.job_id.job_location or ''}</td>
  </tr>
  <tr>
    <td colspan="6">Entr&eacute;e en fonction</td>
  </tr>
<tr>
    <td>d&egrave;s le</td>
    <td style="border:1px solid black">${ cc.date_entry or ''}</td>
    <td>jusqu'au</td>
    <td style="border:1px solid black">${ cc.date_release or ''}</td>
    <td>pour une dur&eacute;e ind&eacute;termin&eacute;e</td>
    <td><input type="checkbox" name="choix1" value="1" /></td>
  </tr>
  <tr>
    <td colspan="6">Dur&eacute;e du travail</td>
  </tr>
  <tr>
    <td colspan="3">l'horaire de travail hebdomadaire s'&eacute;l&egrave;ve &agrave;</td>
    <td colspan="2" style="border:1px solid black">${cc.number_of_hours_worked}</td>
    <td>heures</td>
  </tr>
  <tr>
    <td >Salaire</td>
    <td colspan="6" style="border:1px solid black">${obj.salary}</td>
  </tr>
  
    <td colspan="6"> 1) L'employeur supporte en principe les frais de voyage du travailleur (sauf pour les travailleurs frontaliers), de son lieu dedomicile &agrave; l'&eacute;tranger &agrave; son lieu de travail en Suisse. Ces frais seront rembours&eacute;s au plus tard 3 mois apr&egrave;s l'arriv&eacute;e dutravailleur en Suisse. Ils seront &agrave; la charge du travailleur lorsque ce dernier n'entre pas en service ou qu'il d&eacute;nonce le contratpour des motifs qui lui sont imputables. Les frais de retour sont en r&egrave;gle g&eacute;n&eacute;rale support&eacute;s par le travailleur. Ils sont &agrave; lacharge de l'employeur lorsque le contrat est d&eacute;nonc&eacute; avant terme, pour des motifs qui lui sont imputables, et si le travailleur nepeut prendre un autre emploi en Suisse.</td>
  </tr>
  <tr>
    <td colspan="6"><p>2) Le travailleur conclut une assurance-maladie qui couvre les frais de m&eacute;decin, les m&eacute;dicaments, les s&eacute;jours &agrave; l'h&ocirc;pital ou encure et &eacute;ventuellement la perte de gain. Si ce n'est pas le cas, l'employeur doit conclure une assurance pour le travailleur. Sontr&eacute;serv&eacute;es les r&eacute;glementations cantonales particuli&egrave;res et les &eacute;ventuelles dispositions des conventions collectives ou descontrats-types de travail.Le travailleur doit &ecirc;tre assur&eacute; contre les accidents. Si cela n'est pas d&eacute;j&agrave; le cas en vertu des dispositions l&eacute;gales en vigueur,l'employeur pourvoira lui-m&ecirc;me &agrave; la conclusion de l'assurance-accidents.</p></td>
  </tr>
  <tr>
    <td colspan="6" >3) Lorsque le travailleur est malade sans sa faute et qu'il ne peut travailler, l'employeur paie pour un engagement de plus de 3mois pendant la premi&egrave;re ann&eacute;e de service, le salaire d'au moins 3 semaines, et ensuite, le salaire pour une p&eacute;riode pluslongue fix&eacute;e &eacute;quitablement, compte tenu de la dur&eacute;e des rapports de travail. Un arrangement &eacute;crit peut d&eacute;roger &agrave; cesdispositions, &agrave; condition de garantir au travailleur des prestations pour le moins &eacute;quivalentes.Lorsque le travailleur est assur&eacute; obligatoirement, en vertu d'une disposition l&eacute;gale, contre les cons&eacute;quences &eacute;conomiques d'unem- p&ecirc;chement de travailler qui ne provient pas de sa faute, mais est d&ucirc; &agrave; des raisons inh&eacute;rentes &agrave; sa personne, l'employeurn'est pas tenu de verser le salaire lorsque les prestations d'assurance dues pour le temps limit&eacute; couvrent les quatre cinqui&egrave;mesau moins du salaire aff&eacute;rent &agrave; cette p&eacute;riode.</td>
  </tr>
  <tr>
    <td colspan="6" >4) L'employeur accorde au travailleur, pour chaque ann&eacute;e de service compl&egrave;te, quatre semaines de vacances au moins, et cinqsemaines au moins au travailleur jusqu'&agrave; l'&acirc;ge de 20 ans r&eacute;volus. Une convention collective ou un contrat de travail peut &ecirc;treplus favorable. Pendant l'ann&eacute;e, le droit aux vacances est calcul&eacute; proportionnellement &agrave; la dur&eacute;e des rapports de travail.Si les vacances ne peuvent pas &ecirc;tre prises pendant le dur&eacute;e de l'engagement, l'employeur devra payer au travailleur unsuppl&eacute;ment sur le salaire brut, respectivement d'au moins 8.33 % (4 semaines) et 10.54 % (5 semaines).</td>
  </tr>
  <tr>
    <td colspan="6" >5) La r&eacute;siliation imm&eacute;diate du contrat de travail pour justes motifs, selon l'article 337 du Code des obligations, reste r&eacute;serv&eacute;e.</td>
  </tr>
  <tr>
    <td colspan="6" >6) Les conditions de travail sont pour le reste les m&ecirc;mes que celles des travailleurs suisses ; elles correspondent aux lois envigueur, aux conventions collectives ou aux contrats-type de travail, ou &agrave; toute autre r&eacute;glementation g&eacute;n&eacute;rale, portantnotamment sur les heures suppl&eacute;mentaires, le travail de nuit et du dimanche, les vacances, les indemnit&eacute;s pour les jours f&eacute;ri&eacute;set les &eacute;ventuelles allocations.</td>
  </tr>
  <tr>
    <td colspan="6" >7) L'employeur peut, avec l'accord du travailleur, compenser les heures de travail suppl&eacute;mentaires par un cong&eacute; d'une dur&eacute;e aumoins &eacute;gale, qui doit &ecirc;tre accord&eacute; au cours d'une p&eacute;riode appropri&eacute;e.L'employeur est tenu de r&eacute;tribuer les heures de travail suppl&eacute;mentaires qui ne sont pas compens&eacute;es par un cong&eacute; en versant lesalaire normal major&eacute; d'un quart au moins, sauf disposition contraire figurant dans la convention collective de travail ou lecontrat-type de travail cit&eacute; sous chiffre 4 du contrat.</td>
  </tr>

  <tr>
    <td colspan="6" >Lieu et date:</td>
  </tr>
  <tr>
    <td colspan="6" style="border:1px solid black" >${ obj.employee_id.job_id.job_location} Le ${getDate()}</td>
  </tr>
  <tr>
    <td colspan="3" >L'employeur</td>
    <td colspan="3" >Le travailleur</td>
  </tr>
  
</table>
Ce contrat est associ&eacute; au centre n°${loop.index+1} du contrat n°${len(objects)} 

%endfor
%endfor

</body>
</html>
