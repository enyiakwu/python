# THIS SCRIPT INTEGRATES A REPOSITORY ON GITHUB WITH PULLREQUEST.COM PROJECTS
import requests
import json
import os
import ast
from github import Github

login = os.environ['RD_OPTION_LOGIN']
repo_name = os.environ['RD_OPTION_REPOSITORY_NAME']
API_KEY = os.environ['RD_OPTION_GITHUB_AUTH_TOKEN']
installation_id ="xxxxx"

#g=Github(API_KEY)

# validate the list of repositories - csv input
repo_list = repo_name.split(',')

# fetch repository dump
org_repo = "https://api.github.com/orgs/company-group/repos?page={0}&per_page=100"
true = True

page = 1
org_repo_url = org_repo.format(page)
queue = requests.get(org_repo_url, auth = (login, API_KEY))
queuej = queue.json()
queue = json.dumps(queuej)

# create a file
f = open("repos.txt","w+")
print("done creating dump file")

dic =""
repo_statuscode =""
queuer = requests.get(org_repo_url, auth = (login, API_KEY))

# while page <= 1:
while queuer.text != "[]":
    dic =str(queue.split("{"))
    f.write(dic)
    f.write("\n")
    queuer = requests.get(org_repo_url, auth=(login, API_KEY))
    queuej = queuer.json()
    queue = json.dumps(queuej)
    page =page+1
    org_repo_url =org_repo.format(page)
    #print("running the",page," page")

print("completed dumping orgs repositories \n")
f.close()

rf = open("repos.txt","r")
data = rf.read()

valid_repo = []
invalid_repo = []

# Define function to fetch repository id
def fetch_id(x):
    dic={}
    try:
        m_index = data.index(x)
        # get index of repo name and index number of id key
        valid_repo.append(x)
    except ValueError:
        print ("repository not found in data")
        invalid_repo.append(x)
    else:
        try: 
            m_rev = m_index-200
            m_scrape = data[m_rev:m_index]
            m_index2 = m_scrape.index("id")
            # fetch the second scrape
            match = m_scrape[m_index2-1:m_index]
            m_rev2 = match.rfind(",")
            match2 = match[0:m_rev2]
            matchd = "{"+ match2 +"}" #str(match.split(","))
            dic= ast.literal_eval(matchd)
        except ValueError:
            print ("repository not found in data")
            invalid_repo.append(x)
    return dic

repo_id =""
repo_id_list = []
repo_pair_list = {}

for repo in repo_list:
    repo = repo.strip()
    repo_dic = fetch_id(repo)
    for k, v in repo_dic.items():
        if k == "id":
            repo_id = v
            repo_id_list.append(repo_id)
            repo_pair_list[repo_id] = repo
rf.close()

add_repo_url = "https://api.github.com/user/installations/{0}/repositories/{1}"

status_code =""
repo_statuscode = queuer.status_code
body = ""
if repo_statuscode == 200:
    for repo_id in repo_id_list:
        url = add_repo_url.format(installation_id, repo_id)
        response = requests.put(url, auth=(login, API_KEY))
        status_code = response.status_code
        if status_code == 200:
            body += "Successfully added {0} - to Pullrequest.com.\n".format(repo_pair_list.get(repo_id)) #we found oil
        elif status_code == 204:
            body += "Successfully added {0} - to Pullrequest.com.\n".format(repo_pair_list.get(repo_id)) #"INFO: No content found.\n"       
        elif status_code == 304:
            body += "INFO status{0}: No changes were made to add repository. {1} already exist. Please recheck the repo and submit a new request.\n".format(status_code, repo_pair_list.get(repo_id))
        else:
            body += "Failed to add repo {0} with status code: {1}.\n".format(repo_pair_list.get(repo_id), status_code)        
elif status_code == 404:
    body ="Not found"

print(status_code)
if(len(invalid_repo) == 0):
    str1 = ','.join(valid_repo)
    body += "\nThe repo's were successfully addded to the pullrequest.com as requested, kindly check it from your end and confirm. Below are the list of repo's added to the team, " + '\n' + str1
elif((len(invalid_repo)!= 0) and (len(valid_repo) != 0)):
    str1 = ','.join(valid_repo)
    str2 = ','.join(invalid_repo)
    body += "\nThe repo's "+ str1 + " were added to the pullrequest.com as requested and the below repo's \n failed since the name of the repo is incorrect or it doesn't exist,kindly check and log a new ticket for failed repos with valid repo name \n" + '\n' + str2 
elif((len(invalid_repo) != 0) and (len(valid_repo) == 0)):
    body += "\nRejecting the ticket as there are no valid repo as mentioned on the ticket,please check and log a new ticket with valid names"
print('RD_OUT_body=' + body)

# cleanup file
if os.path.exists("repos.txt"):
    os.remove("repos.txt")
else:
    print("The file does not exist")
