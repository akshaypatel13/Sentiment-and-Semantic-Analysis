import requests
import json
import omdb
import string
import pymongo

# References
#   1. https://gist.github.com/slowkow/7a7f61f495e3dbb7e3d767f97bd7304b
#   2. http://www.omdbapi.com/
#   3. https://stackoverflow.com/questions/39782418/remove-punctuations-in-pandas
#   4. https://stackoverflow.com/questions/20078816/replace-non-ascii-characters-with-a-single-space

movie_url = 'http://www.omdbapi.com/?apikey=6a567bfa&s=%s'
result=[]
result1=[]
keywords = {"Canada","University","Moncton","Halifax","Toronto","Vancouver","Alberta","Niagra"}
for keyword in keywords:
    param=(movie_url%keyword)
    respon = requests.get(param)
    result.append(respon.json())

for res in result:
    for title in res["Search"]:
        movie_data=omdb.get(title=title['Title'])
        movie_data['plot']="".join([ch for ch in movie_data['plot'] if ch not in string.punctuation])
        print(movie_data['plot'])
        if(movie_data['year'].endswith("–")):
           data=movie_data['year'] 
           movie_data['year']=data[:-1]
        print(movie_data['year'])
        result1.append(movie_data)
    

with open('movie_final.json','w') as movies:
    json.dump(result1,movies)
