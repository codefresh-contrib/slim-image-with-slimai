import sys
import os
import requests
import shutil
import json
import time

###########

# Required before Global Vars
def getENV():
    envVar = os.getenv("setENV")
    if envVar == ".docker":
        return "/app"
    else:
        return "."

# Global Variables
templateExecutionPayloadJSONPath = getENV() + "/templates/execution.payload.json"
tmpDir = getENV() + "/tmp"
baseURL = "https://platform.slim.dev"


# Arg Variables
apiToken = sys.argv[1]
orgID = sys.argv[2]
connectorID = sys.argv[3]
digest = sys.argv[4]
namespace = sys.argv[5]
repo = sys.argv[6]
tag = sys.argv[7]
architechture = sys.argv[8]
operatingSystem = sys.argv[9]
pathsList = sys.argv[10]

# Simple list of items in the execution payload JSON to be replaced by the values above
replaceList = [
            'REPLACE.CONNECTOR.ID',                                     # 0
            'REPLACE.IMAGE.DIGEST',                                     # 1
            'REPLACE.IMAGE.NAMESPACE',                                  # 2
            'REPLACE.IMAGE.REPO',                                       # 3
            'REPLACE.IMAGE.TAG',                                        # 4
            'REPLACE.IMAGE.ARCH',                                       # 5
            'REPLACE.IMAGE.OS',                                         # 6
            '{ "REPLACE.ADDITIONAL.FLAGS": "REPLACE.ADDITIONAL.FLAGS" }',  # 7
            '{ "REPLACE.HTTP.PROBE.FLAG": "REPLACE.HTTP.PROBE.FLAG" },',   # 8
            'REPLACE.NAMESPACE.SLIM',                                   # 9
            'REPLACE.REPO.SLIM',                                        # 10
            'REPLACE.TAG.SLIM'                                          # 11
            
            ]

# Perform actions for the tmpDir (i.e create, delete)
def doTmpDir(action):
    if action == "create":
        shutil.rmtree(tmpDir, ignore_errors=True)
        os.mkdir(tmpDir)
    elif action == "delete":
        shutil.rmtree(tmpDir, ignore_errors=True)
    else:
        print("ERROR: Invalid action for doTmpDir()")
        exit(1)

# Creates the flag schemas for the JSON payload in generateRequest()
def createFlags():
    pathsListNew = ""
    createPathSchema = ""
    count = 0
    httpProbeFlag = "{ \"type\": \"flag\", \"name\": \"http-probe-off\", \"value\": \"true\" }"
    if pathsList == "none":
        return "", httpProbeFlag
    for pathsItem in pathsList.split(",", -1):
        count = count + 1
        if count == len(pathsList.split(",", -1)):
            createPathSchema = "{ \"type\": \"flag\", \"name\": \"include-path\", \"value\": \""+pathsItem+"\" }"
        else:
            createPathSchema = "{ \"type\": \"flag\", \"name\": \"include-path\", \"value\": \""+pathsItem+"\" }, "
        pathsListNew = pathsListNew + createPathSchema
    return pathsListNew, httpProbeFlag + ","

# Generates a JSON payload for the execution request in execute()
def generateRequest():
    try:
        with open(templateExecutionPayloadJSONPath, 'r') as file:
            loadTemplateExecPayload = file.read()
    except:
        print("ERROR: Couldn't open Template file for request generation")
        exit(1)
    additionalFlagsSchemas, httpProbeSchema = createFlags()
    loadTemplateExecPayload = loadTemplateExecPayload.replace(replaceList[0], connectorID)
    loadTemplateExecPayload = loadTemplateExecPayload.replace(replaceList[1], digest)
    loadTemplateExecPayload = loadTemplateExecPayload.replace(replaceList[2], namespace)
    loadTemplateExecPayload = loadTemplateExecPayload.replace(replaceList[3], repo)
    loadTemplateExecPayload = loadTemplateExecPayload.replace(replaceList[4], tag)
    loadTemplateExecPayload = loadTemplateExecPayload.replace(replaceList[5], architechture)
    loadTemplateExecPayload = loadTemplateExecPayload.replace(replaceList[6], operatingSystem)
    loadTemplateExecPayload = loadTemplateExecPayload.replace(replaceList[7], additionalFlagsSchemas)
    loadTemplateExecPayload = loadTemplateExecPayload.replace(replaceList[8], httpProbeSchema)
    loadTemplateExecPayload = loadTemplateExecPayload.replace(replaceList[9], namespace)
    loadTemplateExecPayload = loadTemplateExecPayload.replace(replaceList[10], repo)
    loadTemplateExecPayload = loadTemplateExecPayload.replace(replaceList[11], tag + "-slim")
    tmpJSONFilePath = tmpDir + "/execute.json"
    requestJSONFile = open(tmpJSONFilePath, "w")
    requestJSONFile.write(loadTemplateExecPayload)
    requestJSONFile.close()
    try:
        with open(tmpJSONFilePath, 'r') as jsonFile:
            loadTemplateExecPayload = jsonFile.read()
    except:
        print("ERROR: Couldn't open Template file for request generation")
        exit(1)
    return loadTemplateExecPayload

# Sends an execution request to Slim.AI to slim an image
def execute(requestJSONFile):
    print("Executing image hardening for: " + namespace + "/" + repo + ":" + tag)
    executionURL = baseURL + "/orgs/" + orgID + "/engine/executions"
    request = requests.post(executionURL, data = requestJSONFile, auth = ("" , apiToken), headers = {"accept": "application/json", "Content-Type": "application/json"})
    response = request.text
    r = json.loads(response)
    if request.status_code == 400:
        if r['success'] == False:
            print("Failed to upload JSON data: " + r['error'])
            exit(1)
    elif request.status_code != 200:
        print("ERROR: API returned status code during execution post: ", request.status_code)
        exit(1)
    else:
        doTmpDir("delete")
        return r['id']

# Fetches logs for execution and then returns them, or throws an error if the status code != 200
def getLogs(executionID):
    buildURL = baseURL + "/orgs/" + orgID + "/engine/executions/" + executionID + "/log?offset=1374&limit=10000"
    request = requests.get(buildURL, auth = ("", apiToken), headers = {"accept": "application/json", "Content-Type": "application/json"})
    if request.status_code != 200:
        print("ERROR: API returned status code during log fetch: ", request.status_code)
        exit(1)
    else:
        return request.text

# Watches for changes in the execution status
def watch(executionID):
    buildURL = baseURL + "/orgs/" + orgID + "/engine/executions/" + executionID
    request = requests.get(buildURL, auth = ("", apiToken), headers = {"accept": "application/json", "Content-Type": "application/json"})
    response = request.text
    if request.status_code != 200:
        print("ERROR: API returned status code during watch: ", request.status_code)
        exit(1)
    else:
        r = json.loads(response)
        completionStatus = "completed"
        failureState = "failed"
        # Watches for statuses mentioned above, when met, result(<execution-id>,isFailedStatus)
        while r['state'] != completionStatus:
                time.sleep(5)
                request = requests.get(buildURL, auth = ("", apiToken), headers = {"accept": "application/json", "Content-Type": "application/json"})
                if request.status_code != 200:
                    print("ERROR: API returned status code during watch: ", request.status_code)
                    exit(1)
                else:
                    response = request.text
                    r = json.loads(response)
                    print("ID: " + executionID)
                    print("Status: " + r['state'])
                    if r['state'] == failureState:
                        result(executionID, True)
                    else:
                        print("-")
                        print(getLogs(executionID))
                        print("------------------")
        result(executionID, False)


# Displays execution results once the execution has finished (either failed or completed)
def result(executionID, isFailedStatus):
    print("========= RESULTS ==========")
    if isFailedStatus:
        buildURL = baseURL + "/orgs/" + orgID + "/engine/executions/" + executionID + "/events"
    else:
        buildURL = baseURL + "/orgs/" + orgID + "/engine/executions/" + executionID + "/result"
    request = requests.get(buildURL, auth = ("", apiToken), headers = {"accept": "application/json", "Content-Type": "application/json"})
    response = request.text
    if request.status_code != 200:
        print("ERROR: API returned status code during result fetch: ", request.status_code)
        exit(1)
    else:
        r = json.loads(response)
        if isFailedStatus:
            print("ERROR: Execution has failed.")
            print("Please see events below for details")
            print("---------- EVENTS ----------")
            print(response)
            exit(1)
        else:
            print("Image hardened successfully. (" + namespace + "/" + repo + ":" + tag + "-slim)")
            exit()

if __name__ == "__main__":
    # Create tmpDir
    doTmpDir("create")
    # Create flags schemas for JSON payload
    createFlags()
    # Generates JSON payload for execution
    getRequestJSONFile = generateRequest()
    # Sends an execution to Slim.AI then returns execution ID to watch()
    getExecutionID = execute(getRequestJSONFile)
    # Watches for changes on execution ID, sends results to result()
    watch(getExecutionID)
