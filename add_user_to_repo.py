# THIS SCRIPT ADDS A USER OR COLLABORATOR (SINGLE OR AS A CSV LIST) TO A GITHUB REPOSITORY
import requests, json
import authfile
from slugify import slugify


"""
Add user to Repository
"""

#login = "@option.login@"
#members_list = "@option.member_list@"
#password = "@option.password@"
#repo_name = "@option.repo_name@"
#permission = "@option.permission@"

# validate repo name input is lowercase
repo_name_slug = repo_name.replace(" ", "-").lower() 
slugify(repo_name, lowercase=True)
members = members_list.split(',')

# permission validation according to Github permission convention
if permission == "admin":
    data = {
    "permission": "admin"
    }
elif permission == "read":
    data = {
    "permission": "pull"
    }    
else:
    data = {
    "permission": "push"
    }

comment = ''

# Validate for either repo URL or repository name alone
if "company-group/" in repo_name_slug:
    repo_only= repo_name_slug.rpartition("company-group/")[-1]
    repo_get_url= "https://api.github.com/repos/company-group/{0}".format(repo_only)
    repo_name_slug= repo_get_url
    repo_add_member_url="{0}/collaborators/{1}"
else:
    repo_get_url="https://api.github.com/repos/company-group/{0}".format(repo_name_slug)
    repo_add_member_url="https://api.github.com/repos/company-group/{0}/collaborators/{1}"

# check that repo exists or repo value entered is correct
response = requests.get(repo_get_url, auth=(login, password))
status_code = response.status_code
print('Repo found: {0}'.format(status_code)) #get repo response

# if repo exists, then add member(s) to repository
if status_code == 200:
    count = 1
    for member in members:
        url = repo_add_member_url.format(repo_name_slug, member.strip())
        response = requests.put(url, data=json.dumps(data), auth=(login,password))
        status_code = response.status_code
        if status_code == 201:
            comment += "Successfully added {0} - user has been invited to collaborate.\n".format(member) #we found oil
            if len(members) <= count:
                break
            else:
                count += count
                print(count) 
                continue
        elif status_code == 204:
            comment += "Successfully added {0} - user is now a collaborator.\n".format(member)        
        elif status_code == 404:
            comment = "Failed to add user {0} as user does not exist. Please recheck the username and submit a new request.\n".format(member, status_code)
        else:
            comment = "Failed to add user {0} with status code: {1}.\n".format(member, status_code)        
elif status_code == 404:
    comment = "Failed to find repo {0}. Check for any typo and submit a new request.\n".format(repo_name_slug, status_code)

else:
    comment = "Failed to get repo {0} with status code: {1}.".format(repo_name_slug, status_code)

if status_code == 201:
    comment += "\nCompleted processing your request, please approve this issue as resolved.\nThank you."
elif status_code == 204:
    comment += "\nCompleted processing your request, please approve this issue as resolved.\nThank you."
else:
    comment += "\nPlease recheck the format of information entered and raise another ticket"
    
print("output: " + comment)
# print("RD_OUT_comment=" + comment)
