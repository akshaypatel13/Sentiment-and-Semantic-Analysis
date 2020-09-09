import requests
import json
import pandas
import re
import string


# References
#   1. https://gist.github.com/slowkow/7a7f61f495e3dbb7e3d767f97bd7304b
#   2. https://newsapi.org/docs/get-started
#   3. https://stackoverflow.com/questions/39782418/remove-punctuations-in-pandas
#   4. https://stackoverflow.com/questions/20078816/replace-non-ascii-characters-with-a-single-space



header = {'Authorization': '87358bc6a9d0436684c5c57b907223b4'}
news_url = 'https://newsapi.org/v2/everything'



emj_pat = re.compile("["
        u"\U0001F600-\U0001F64F"  
        u"\U0001F300-\U0001F5FF"  
        u"\U0001F680-\U0001F6FF"  
        u"\U0001F1E0-\U0001F1FF"  
                           "]+", flags=re.UNICODE)  


keywords = {'q': 'Canada OR University OR Dalhousie University OR Halifax OR Canada Education OR Moncton OR Toronto','pageSize':'100'}

resp = requests.get(url = news_url, headers = headerp,arams = keywords)
out_json = json.dumps(resp.json(), indent = 4)
y=json.loads(out_json)
df=y['articles']
print(type(df))

for key in df:
    if(key['content']!=None):
        content=key['content'].lower()
        clean_content="".join([ch for ch in content if ch not in string.punctuation])
        clean_content=clean_content.replace("\r","")
        clean_content=clean_content.replace("\n","")
        cleaned="".join(i for i in clean_content if ord(i)<128)
        cleaned_final=emojipattern.sub(r'',cleaned)
        
        key['content']=cleaned_final
print(df)
with open('news_final.json','w') as news:
    json.dump(df,news)









