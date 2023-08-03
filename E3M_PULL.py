from psdi.mbo import MboConstants, MboRemote, MboSetRemote
from psdi.security import UserInfo
from psdi.server import MXServer
from java.io import OutputStream
from java.io import InputStreamReader
from java.lang import StringBuilder
from java.io import BufferedReader
from java.io import IOException
from java.net import HttpURLConnection
from java.net import URL
from java.util import Base64
from java.lang import String
from java.io import FileWriter
from psdi.util.logging import MXLoggerFactory

logger = MXLoggerFactory.getLogger("maximo.script.GIT");
logger.debug(" Start E3M_PULL");

def fetch_file_content_from_github(url,gitHubToken):
    #java_url = URL(str(github_raw_url))
    conn = url.openConnection()
    #con= url.openConnection()
    conn.setRequestMethod("GET");
    conn.setRequestProperty("Content-Type", "application/json")
    conn.setRequestProperty("Authorization", "Bearer" + gitHubToken)

    input_stream = conn.getInputStream()
    input_reader = BufferedReader(InputStreamReader(input_stream))
    content = ""
    line = input_reader.readLine()
    while line is not None:
        content += line + "\n"
        line = input_reader.readLine()

    input_reader.close()
    conn.disconnect()
    return content
    raise TypeError(content)
    

autoscriptName=mbo.getString("AUTOSCRIPT")
source=mbo.getString("SOURCE")
sourceCode=Base64.getEncoder().encodeToString(String(source).getBytes("UTF-8"));

gitHubApi=MXServer.getMXServer().getProperty("e3m.github.api")+autoscriptName+".py"
gitHubToken=MXServer.getMXServer().getProperty("e3m.github.token")
gitHubCode=MXServer.getMXServer().getProperty("e3m.github.download.url")+autoscriptName+".py"

url = URL(gitHubCode)
con= url.openConnection()
con.setRequestMethod("GET");
con.setRequestProperty("Content-Type", "application/json")
con.setRequestProperty("Authorization", "Bearer" + gitHubToken)
statusCode = con.getResponseCode();

if launchPoint == "E3M_PULL":
    #autoscriptName=mbo.getString("AUTOSCRIPT")
    #gitHubCode=MXServer.getMXServer().getProperty("e3m.github.download.url")+autoscriptName+".py"
    if (statusCode == 200):
        
        logger.debug("gitHubCode "+gitHubCode);

        input_stream = con.getInputStream()
        input_reader = BufferedReader(InputStreamReader(input_stream))
        content = ""
        line = input_reader.readLine()
        while line is not None:
            content += line + "\n"
            line = input_reader.readLine()
    
        input_reader.close()
        
        #data = fetch_file_content_from_github(github_raw_url,gitHubToken)
        data = content
        logger.debug("data "+data);
        
        if data:
            
            #e3msScripSet=mbo.getMboSet("e3mautoscript")
            e3msScripSet = MXServer.getMXServer().getMboSet("E3MAUTOSCRIPT", mbo.getUserInfo())
            e3msScripSet.setWhere("AUTOSCRIPT='"+autoscriptName+"'")
            e3msScripSet.reset()
            if(e3msScripSet.isEmpty()):
                e3msScript=e3msScripSet.add()
                e3msScript.setValue("source",data,MboConstants.NOACCESSCHECK)
                e3msScript.setValue("autoscript",autoscriptName,MboConstants.NOACCESSCHECK)
                #e3msScript.setValue("pull",1,MboConstants.NOACCESSCHECK)
                #e3msScript.setValue("push",0,MboConstants.NOACCESSCHECK)
                e3msScripSet.save()
            else:
                e3msScript=e3msScripSet.getMbo(0)
                #e3msScript.setValue("pull",1,MboConstants.NOACCESSCHECK)
                #e3msScript.setValue("push",0,MboConstants.NOACCESSCHECK)
                e3msScript.setValue("source",data,MboConstants.NOACCESSCHECK)
                e3msScripSet.save()
                #params = [data]
                #service.error("CI", "invalidassetforci", params)
            
        else:
            print("Failed to fetch data from GitHub.")

con.disconnect()