#Script Name     : E3M_TECH_SRPUSHNOTIFICATION
#Purpose         : Send push notification to e3mtechnician group when ever SR is created
#Launch Point    : SR Object and OWNER , OWNERGROUP ATTRIBUE of SR object
#Version         : 1.0
#Condition       : status in ('NEW','QUEUED')
#Last Modified  Comment:  
#1) 14-05-2020: SendFCMnotifcation Client Updated with Java Client and Apache client is been removed
#2) Instance Topic Dev Server Format: Sys property mxe.e3m.mobile.firebase.fcminstance value "coh-dev" 

from java.io import IOException
from psdi.util.logging import MXLogger
from psdi.util.logging import MXLoggerFactory
from java.rmi import RemoteException
from com.ibm.json.java import JSONArray
from com.ibm.json.java import JSONObject
from psdi.mbo import MboRemote
from psdi.mbo import  MboSet
from psdi.mbo import MboSetRemote
from psdi.server import MXServer 

from java.net import HttpURLConnection   #new java Client library for Send Notifications
from java.net import URL
from java.io import OutputStream

def SendFCMnotification(entity,fcmurl,serverkey):
    url = URL(fcmurl)
    con = url.openConnection()
    con.setRequestMethod('POST')
    con.setRequestProperty('Content-Type', 'application/json; utf-8')
    con.setRequestProperty('Accept', 'application/json')
    con.setRequestProperty("AUTHORIZATION", serverkey)
    con.setDoOutput(True)
    os = con.getOutputStream()
    os.write(str(entity))
    os.flush()
    os.close()
    responseCode = con.getResponseCode()



print 'Owner SR Notification check'
#log = MXLoggerFactory.getLogger("maximo.e3mfcm")
#log.debug("**********SR Owner Push*********")
inst_topic = "/topics/";
objIos =  JSONObject();
chobjIos =  JSONObject();
chobjIosNotification = JSONObject();
chobjIosdata =JSONObject();
ticketId= mbo.getString("TICKETID");
ticketUid= mbo.getInt("TICKETUID");               
srDesc= mbo.getString("DESCRIPTION");
owner=mbo.getString("OWNER");
user=None;

if (mbo.isNull("OWNER")==True):
    ownergroup=mbo.getString("OWNERGROUP");
    print'ownergroup is ............................:'+ownergroup
    if (ownergroup is not None):
       persongroupSet = mbo.getMboSet("E3MSROWNERGROUP");
       persongroupmbo = persongroupSet.getMbo(0);
       if (persongroupmbo is not None):
         TeamSet=persongroupmbo.getMboSet("ALLPERSONGROUPTEAM");
         teamsetcout=TeamSet.count();
         print'teamsetcout is not Empty , count is ' +str(teamsetcout)
         for i in range (0, teamsetcout):
          membermbo = TeamSet.getMbo(i);
          perSet    = membermbo.getMboSet("RESPPARTYGROUP_PERSONS");
          personmbo = perSet.getMbo(0);         
          if (personmbo is not None):
              UserSet     = personmbo.getMboSet("USER");
              usermbo     = UserSet.getMbo(0);          
              if (usermbo is not None):                             
                             user=usermbo.getInt("MAXUSERID")
                             e3mTechnicianGroupuserSet=MXServer.getMXServer().getMboSet("GROUPUSER", MXServer.getMXServer().getSystemUserInfo());
                             whereClause="groupname in('E3MTECHNICIAN','E3MSUPERVISOR','E3MSTOREKEEPER','E3MMANAGER') and userid='"+usermbo.getString("USERID")+"'"
                             e3mTechnicianGroupuserSet.setWhere(whereClause);
                             e3mTechnicianGroupuserSet.reset();
                             if (e3mTechnicianGroupuserSet.isEmpty()== False):                                 
                                 chobjIos.put("ticketid",ticketId);
                                 chobjIos.put("type","SR");
                                 chobjIosNotification.put("title" , "SR# "+str(ticketId)+" is assigned");
                                 chobjIosNotification.put("body" ,srDesc);
                                 objIos.put("data",chobjIos);
                                 configData = MXServer.getMXServer().getConfig();
                                 finst = configData.getProperty("mxe.e3m.mobile.firebase.fcminstance");
                                 if finst is not None:
                                  inst_topic= inst_topic + finst + '-';
                                 else:
                                  inst_topic= inst_topic+'-';
                                 objIos.put("to",inst_topic+str(user)) ;
                                 objIos.put("notification",chobjIosNotification);
                                 #objIos.put("content_available",True); 
                                 fcmUrl="https://fcm.googleapis.com/fcm/send";
                                 fcmkey = configData.getProperty("mxe.e3m.mobile.firebase.serverkey");                                
                                 jsonStrIos = objIos.serialize(True)                                 
                                 SendFCMnotification(jsonStrIos, fcmUrl,fcmkey)
                                 e3mTechnicianGroupuserSet.close();                                              
else :
    maxUserdetailsSet=mbo.getMboSet("$E3MMAXUSERDETAILS", "MAXUSER", "USERID = '"+owner+"'");
    if(maxUserdetailsSet.isEmpty()== False): 
       maxUserdetailsMbo=maxUserdetailsSet.getMbo(0);
       user=maxUserdetailsMbo.getInt("MAXUSERID")       
       e3mTechnicianGroupuserSet=MXServer.getMXServer().getMboSet("GROUPUSER", MXServer.getMXServer().getSystemUserInfo());
       whereClause="groupname in('E3MTECHNICIAN','E3MSUPERVISOR','E3MSTOREKEEPER','E3MMANAGER') and userid='"+owner+"'"       
       e3mTechnicianGroupuserSet.setWhere(whereClause);
       e3mTechnicianGroupuserSet.reset();
       if(e3mTechnicianGroupuserSet.isEmpty()== False):
          chobjIos.put("srid",ticketUid);
          chobjIos.put("ticketid",ticketId);
          chobjIos.put("type","SR");
          chobjIosNotification.put("title" , "SR# "+str(ticketId)+" is assigned");
          chobjIosNotification.put("body" ,srDesc);          
          objIos.put("data",chobjIos);
          configData = MXServer.getMXServer().getConfig();
          finst = configData.getProperty("mxe.e3m.mobile.firebase.fcminstance");
          if finst is not None:
            inst_topic= inst_topic + finst + '-';
          else:
            inst_topic= inst_topic + '-';
          objIos.put("to",inst_topic+str(user)) ;
          #objIos.put("to","/topics/"+"coh-dev-"+str(user)) ;
          objIos.put("notification",chobjIosNotification);
          #objIos.put("content_available",True);  
          fcmUrl="https://fcm.googleapis.com/fcm/send";
          fcmkey = configData.getProperty("mxe.e3m.mobile.firebase.serverkey");
          jsonStrIos = objIos.serialize(True)          
          SendFCMnotification(jsonStrIos, fcmUrl,fcmkey)
          e3mTechnicianGroupuserSet.close();
          maxUserdetailsSet.close();