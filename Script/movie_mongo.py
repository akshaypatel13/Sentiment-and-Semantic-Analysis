import json
import pymongo
mongo_client=pymongo.MongoClient("mongodb://akshay:root@18.224.137.236/admin")
db_connection=mongo_client.admin
collection_mongo=db_connection['movies_f']
with open('movie_final.json','r') as tweets_final:
    result=tweets_final.read()
    collection_mongo.insert_many(json.loads(result))
    
