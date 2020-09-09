import pandas as pd
import json
from beautifultable import BeautifulTable


result1=[]
with open('fintweetss1.json','r') as tweet:
    result1=json.load(tweet)


print(result1)
pos=[]

final_append=[]
with open('positive.txt','r') as positive:
    for i in positive:
        pos.append(i.strip())
neg=[]
with open('negative.txt','r') as negative:
    for i in negative:
        neg.append(i.strip())


dic=[]
for tw in result1:
    dict1={}
    tweet_text=tw['Tweet']
    twt_list=tweet_text.split(" ")

    for i in twt_list:
        count=twt_list.count(i)
        dict1[i]=count
        
    dic.append(dict(dict1))

table = BeautifulTable()
table.column_headers=['Tweet','Message/Tweets','Match','Polarity']
print(dic)
i=0

list_tweet=[]
for twe_text in result1:
    list_tweet.append(twe_text['Tweet'])
print(list_tweet)


col=['Word','Frequency','Polarity']
df = pd.DataFrame(columns = col)
pos_list=[]
neg_list=[]
final_dic={}
for twi in dic:
    polarity=''
    pos_dic={}
    neg_dic={}
    pos_count=0
    neg_count=0
    matched_words_pos=[]
    matched_words_neg=[]
    for word in twi:
        if word in pos:
            freq=twi.get(word)
            pos_dic[word]=freq
            df = df.append({"Word": word,"Frequency":freq,"Polarity":'positive'},ignore_index=True)
            matched_words_pos.append(word)
            pos_count+=freq
        elif word in neg:
            freq=twi.get(word)
            neg_dic[word]=freq
            #print(word+":"+str(freq))
            df = df.append({"Word": word,"Frequency":freq,"Polarity":'negative'},ignore_index=True)           
            matched_words_neg.append(word)
            neg_count+=freq
    pos_list.append(pos_dic)
    neg_list.append(neg_dic)
    if(pos_count>neg_count):
        polarity='positive'
        table.append_row([i,list_tweet[i],matched_words_pos,polarity])
            
    elif(neg_count>pos_count):
        polarity='negative'
        table.append_row([i,list_tweet[i],matched_words_neg,polarity])
            
    else:
        polarity='neutral'
        table.append_row([i,list_tweet[i],'No match',polarity])
         
    i+=1
    

final_list_pos={}
final_list_neg={}
print(table)
print("------------------------------------------------------------")

print("-----------------pos-------------------------------------------")


print("------------------------------------------")
for poss in pos_list:
    for i in list(poss.keys()):
        if i in list(final_list_pos.keys()):
            final_list_pos[i]=int(final_list_pos.get(i))+1
        else:
            final_list_pos[i]=int(poss.get(i))
    
print(final_list_pos)


print("--------------------neg----------------------------------------")
print(neg_list)

print("------------------------------------------")
for negg in neg_list:
    for i in list(negg.keys()):
        if i in list(final_list_neg.keys()):
            final_list_neg[i]=int(final_list_neg.get(i))+1
        else:
            final_list_neg[i]=int(negg.get(i))


print(final_list_neg)

print("-------------neg_to_dataframe----------------------")

df_words = pd.DataFrame(columns=['Word', 'Frequency', 'Polarity'])
for i in final_list_neg:
    df_words=df_words.append({'Word':i,'Frequency':final_list_neg.get(i),'Polarity':'Negative'}, ignore_index=True)


print("-------------pos_to_dataframe----------------------")


for i in final_list_pos:
    df_words=df_words.append({'Word':i,'Frequency':final_list_pos.get(i),'Polarity':'Positive'}, ignore_index=True)
print(df_words)

df_words.to_csv('output_words.csv',index=False)

print("-------------------text---------------------")

with open('word.txt', 'w') as write_txt:
    write_txt.write(str(table))

