import json
import requests
from requests.auth import HTTPBasicAuth 
import re
import time
import pandas as pd 
import os
token = os.getenv('GITHUB_TOKEN', 'a631efb5a58c7fb9d2e509384f13146058b4b1f0')
headers = {'Authorization': f'token {token}'} 
k=0
namedata=[]
emaildata=[]
nm=''
try:
    for j in range (400):
        url="https://api.github.com/repos/laravel/laravel/stargazers?per_page=100&page="+str(j)
        responce=requests.get(url,headers=headers)
        k+=1
        print("request"+str(k))
        data1=responce.json()
        for i in data1:
            nm=i["login"]
            nameurl="https://api.github.com/users/"+i["login"]#get the login name
            
            nresponce=requests.get(nameurl,headers=headers)
            data=nresponce.json()
            

            emurl='https://api.github.com/users/'+i["login"]+'/events/public'#get the email json
            
            eresponce=requests.get(emurl,headers=headers)
            edata=eresponce.json()
            email=json.dumps(edata)
            if 'email'in email:#check if emil exist or not
                
                e=re.search(r'[\w\.-]+@[\w\.-]+', email)#extract email
                if e:
                    #time.sleep(10)
                    print('inside if')
                    emaildata.append(str(e.group(0)))
                    namedata.append(str(data["name"]))
                        
except Exception as ex:
    print("error="+str(ex))
    print(nm)
finally:

    d={'name':namedata,'email':emaildata}
    df = pd.DataFrame(d)
    # saving the dataframe 
    df.to_csv('file1.csv') 
    print("done")

#for each entry 3 api call are going on so after some time get blocked
#so i hv used a break after 25 api calls