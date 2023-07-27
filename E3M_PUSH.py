from psdi.mbo import MboConstants
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
from java.io import BufferedReader, InputStreamReader

autoscriptName=mbo.getString("AUTOSCRIPT")
gitHubCode=MXServer.getMXServer().getProperty("e3m.github.download.url")+autoscriptName+".py"

def fetch_file_content_from_github(github_raw_url):
    java_url = URL(str(github_raw_url))
    conn = java_url.openConnection()
    #url = URL(github_raw_url)
    #conn = url.openConnection()

        # Open the input stream and read the content
    input_stream = conn.getInputStream()
    input_reader = BufferedReader(InputStreamReader(input_stream))
    content = ""
    line = input_reader.readLine()
    while line is not None:
        content += line + "\n"
        line = input_reader.readLine()

    input_reader.close()
    #raise TypeError(content)
    return content
    #except Exception as e:
        #print(f"An error occurred: {e}")
     #   return None

# Example usage in Maximo Automation Script:
github_raw_url = URL(gitHubCode)
data = fetch_file_content_from_github(github_raw_url)
#raise TypeError(data)
if data:
    print("File content from GitHub:")
    service.log(data)
else:
    print("Failed to fetch data from GitHub.")





def extractSHA(responseBody):
    sha_start_index = responseBody.find("\"sha\":\"") + 7
    sha_end_index = responseBody.find("\"", sha_start_index)
    #raise TypeError(responseBody[sha_start_index:sha_end_index])
    return responseBody[sha_start_index:sha_end_index]
    

autoscriptName=mbo.getString("AUTOSCRIPT")
source=mbo.getString("SOURCE")
sourceCode=Base64.getEncoder().encodeToString(String(source).getBytes("UTF-8"));

gitHubApi=MXServer.getMXServer().getProperty("e3m.github.api")+autoscriptName+".py"
gitHubToken=MXServer.getMXServer().getProperty("e3m.github.token")
gitHubCode=MXServer.getMXServer().getProperty("e3m.github.download.url")+autoscriptName+".py"

url = URL(gitHubApi)
con= url.openConnection()
con.setRequestMethod("GET");
con.setRequestProperty("Content-Type", "application/json")
con.setRequestProperty("Authorization", "Bearer " + gitHubToken)
statusCode = con.getResponseCode();


if (statusCode == 200 or dstatusCode == 200):
    reader = BufferedReader(InputStreamReader(con.getInputStream()));
    response = StringBuilder();
    line = reader.readLine();
    while (line is not None):
        response.append(line);
        line = reader.readLine();
        
    #reader.close();
    
    responseBody = response.toString();
    #mbo.setValue("source",responseBody);
    sha = extractSHA(responseBody);
    params = [sha]
    #service.error("access", "field", params)
    githubcontent = String.format("{\"message\": \"Update file\", \"content\": \"%s\", \"sha\": \"%s\"}", sourceCode, sha);
    conUpdate= url.openConnection()
    conUpdate.setRequestMethod("PUT");
    conUpdate.setRequestProperty("Content-Type", "application/json")
    conUpdate.setRequestProperty("Authorization", "Bearer " + gitHubToken)
    conUpdate.setDoOutput(True)
    os = conUpdate.getOutputStream()
    content=String(githubcontent).getBytes("UTF-8")
    os.write(content)
    os.flush()
    os.close()
    responsecode=conUpdate.getResponseCode()
    conUpdate.disconnect()

else:
    githubcontent = String.format("{\"message\":\"Add file\",\"content\":\"%s\"}",sourceCode);
    conCreate= url.openConnection()
    conCreate.setRequestMethod("PUT");
    conCreate.setRequestProperty("Content-Type", "application/json")
    conCreate.setRequestProperty("Authorization", "Bearer " + gitHubToken)
    conCreate.setDoOutput(True)
    
    os = conCreate.getOutputStream()
    content=String(githubcontent).getBytes("UTF-8")
    os.write(content)
    os.flush()
    os.close()
    
    responsecode=conCreate.getResponseCode()
    conCreate.disconnect()