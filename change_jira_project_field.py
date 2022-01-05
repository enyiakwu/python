# CREATE OR UPDATE JIRA PROJECT FIELD
import requests, json
import authfile

#project_key = "TST"
project_key= "TST"
project_name = "TestProject"
project_field = "SaaS VP"
new_value = "unassigned"

# Add your JIRA username and password below
username= authfile.username()
password= authfile.password()

project_key = project_key.upper()

# capture unassigned value to remove user
new_value = new_value.lower()
null=None
if new_value =="unassigned":
    new_value={
        "value":null
        }
else:
    new_value= new_value

# get username display name details
user_URL = "https://jira.devfactory.com/rest/api/2/user?username={0}".format(new_value)
userR = requests.get(user_URL, auth=(username, password))
userjson = userR.json()

displayName = new_value
for key, value in userjson.items():
    if key == "displayName":
        fullName=value
        displayName= "Successfully added {0} to".format(fullName)
        break
    else:
        displayName="Successfully unassigned user from"
        print("display name not found")
# data to be sent to Jira comment
comment=""

# Getting the profield id
url= "http://jira.devfactory.com/rest/profields/api/2.0/fields"
response2= requests.get(url, auth=(username, password))
status_code=response2.status_code
print("retrieved profield fields with status: {0}".format(status_code))
response3= response2.json()
for i in response3:      
    if i["name"] == project_field:
        print("found project field: " + i["name"])
        fieldid = i["id"]
        print (fieldid)
        break
    else:
        print("didn't find" + i["name"]) 

headers={
    "Content-Type": "application/json"
}
new_profield_url='https://jira.devfactory.com/rest/profields/api/2.0/values/projects/{0}/fields/{1}'

if status_code == 200:
    # Defining payload and setting the profield
    url=new_profield_url.format(project_key, fieldid)
    new_response=requests.post(url, auth=(username, password),headers=headers, data=json.dumps(new_value))
    print(new_response)
    print(new_response.text)
    status_code2=new_response.status_code
    if status_code2 == 200:
        comment+= "\n{0} the project field {1}\n".format(displayName, project_field)
    else:
        status_code2=new_response.status_code
else:
    print(status_code2)

if status_code2 == 200:
    comment+="\nCompleted processing your request, please confirm and approve this ticket as resolved.\nThank you."
elif status_code2 == 400:
    comment="\nRequest invalid, failed to update project field {0}, \nThe username or new value might be invalid. \nPlease reopen a new ticket with a valid name.\n".format(project_field)
elif status_code2 == 401:
    comment="\nnot Authorized"
elif status_code2 == 500:
    comment="\nInternal Error"
else:
    comment="\nFailed to execute operation, with status code: {0} the project key is likely invalid, check and reopen a new ticket.".format(status_code2)

print("output: " + comment)

#print("RD_OUT_body=" + body)
