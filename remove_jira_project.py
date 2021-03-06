#!/usr/bin/python3
import requests, json
import authfile

# define input variables
jira_system = "Central Jira"
project_key= "TESS"
project_name = "Test2Rem3"

# validate that project key variable is BLOCK CASE
project_key = project_key.upper()

# fetch OAuth token from auth module file
auth = authfile.username()
token = authfile.token()
comment = ""

# Getting the project
url= "https://jira.company.com/rest/api/2/project/{0}".format(project_key)
response1= requests.get(url, auth=(auth, token))
status_code=response1.status_code

# validate status codes
if status_code == 200:
    print("project exists with status: {0}".format(status_code))
else: 
    print("project not found, with status: {0}".format(status_code))
    comment="Project does not exist."

headers={
    "Content-Type": "application/json"
}

rem_project_url= url
if status_code == 200:
    #Delete the project
    new_response=requests.delete(rem_project_url, auth=('enyinnaya.akwu', password),headers=headers)
    print(new_response)
    print(new_response.text)
    status_code2=new_response.status_code
    if status_code2 == 204:
        comment+= "Successfully deleted the project {0} from CENTRAL JIRA.".format(project_key)
    else:
        status_code2=new_response.status_code
        comment+="Failed to remove project {0}.".format(project_key)
else:
    print(status_code)

if status_code2 == 204:
    comment+="\nCompleted processing your request, please confirm and approve this ticket as resolved.\nThank you."
elif status_code2 == 401:
    print("login with authorized user and re-run command")
elif status_code2 == 403:
    comment+="\nUser not authorized to delete project.\n"
elif status_code2 == 404:
    comment+="\nProject does not exist. \nPlease reopen a new ticket with a valid project ID"
else:
    comment+="\nFailed to fully execute operation, please reopen a new ticket with valid details"

print("output: " + comment)

#print("RD_OUT_body=" + body)
