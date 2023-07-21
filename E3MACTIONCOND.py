/*Purpose		        : Validate WF Action Based on SQL Conditions
Version        	        : 1.0 
Create By			    : EAM360 Team 
Last Modified By	    : Lokesh
Last Modified Date	    : 2023-APR-19 
Last Modified Comment	: Included author section and woSet.close(), wfactionSet.close()
API Name              	: Not Applicable
Customer                : PNNL
*/

load("nashorn:mozilla_compat.js");

importClass(Packages.psdi.server.MXServer);
importClass(Packages.psdi.common.parse.ParserService);
importClass(Packages.psdi.mbo.SqlFormat);

var response = {};
var responseBody;
var workorderid = request.getQueryParam("ownerid");
var actionid=request.getQueryParam("actionid");
var wfactionid=request.getQueryParam("wfactionid");

var userInfo = MXServer.getMXServer().getSystemUserInfo();
var sqf = new SqlFormat(userInfo, "actionid=:1 and wfactionid=:2 ");
sqf.setObject(1, "WFACTION", "actionid", actionid);
sqf.setObject(2, "WFACTION", "wfactionid", wfactionid);
var wfactionSet =  MXServer.getMXServer().getMboSet("WFACTION", userInfo);
wfactionSet.setWhere(sqf.format());
wfactionSet.reset();
var wfactionMbo = wfactionSet.getMbo(0);
var sql=wfactionMbo.getString("condition");
if(sql.length>0)
{
	var sqf1 = new SqlFormat(userInfo, "workorderid=:1");
	sqf1.setObject(1, "WORKORDER", "workorderid", workorderid);
	var woSet = MXServer.getMXServer().getMboSet("WORKORDER", userInfo);
	woSet.setWhere(sqf1.format());
	woSet.reset();
	if(woSet.isEmpty())
	{
		response.e3mavailable=true;
	}
	else
	{
		var woMbo = woSet.getMbo(0);
		var parServ=MXServer.getMXServer().lookup("PARSER");
		var avalbl = parServ.getBoolean(sql,woMbo);	
		response.e3mavailable=avalbl;	
	}
	woSet.close();
}
responseBody = JSON.stringify(response);
wfactionSet.close();