import json
import pymongo
mongo_client=pymongo.MongoClient("mongodb://akshay:root@18.224.137.236/admin")
db_connection=mongo_client.admin
collection_mongo=db_connection['tweets']
with open('tweets.json','r') as tweet:
    result=tweet.read()
    collection_mongo.insert_many(json.loads(result))
