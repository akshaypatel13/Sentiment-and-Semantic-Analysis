import requests
import json
import pandas as pd
import re
import string
from beautifultable import BeautifulTable
import math

# References
#   1. https://beautifultable.readthedocs.io/en/latest/



news=[]
with open('news_finall.json','r') as news_sing:
    news=json.load(news_sing)


length=len(news)
print(length)


canada_count=0
halifax_count=0
dal_count=0
uni_count=0
bus_count=0




for i in range(0,length):
    with open('file%s.txt' % i, 'r') as words:
        abcd=words.read()
    if 'dalhousie university' in abcd:
        dal_count+=1
    if 'canada' in abcd:
        canada_count+=1
    if 'university' in abcd:
        uni_count+=1
    if 'halifax' in abcd:
        halifax_count+=1
    if 'business' in abcd:
        bus_count+=1
    

print('Canada:'+str(canada_count)+'university:'+str(uni_count)+'dalhousie university:'+str(dal_count)+'halifax:'+str(halifax_count)+'business:'+str(bus_count))
    

table = BeautifulTable()

table.column_headers=['Search Query','Document containing term(df)','Total documents(N)/number of documents term appeared (df)','Log10(N/df)']


# Canada
table.append_row(['Canada',canada_count,length/canada_count,math.log10(length/canada_count)])
#Halifax
table.append_row(['Halifax',halifax_count,length/halifax_count,math.log10(length/halifax_count)])
#University
table.append_row(['University',uni_count,length/uni_count,math.log10(length/uni_count)])
#Business
table.append_row(['Business',bus_count,length/bus_count,math.log10(length/bus_count)])
#Dalhousie University
table.append_row(['Dalhousie University',dal_count,length/dal_count,math.log10(length/dal_count)])
        
print(table)



# part2

print("-----------------------2---------------------------------")


f_dict={}
f_list=[]
table1 = BeautifulTable()

table1.column_headers=['Canada appeared in','Total words(m)','Frequency(f)']
word_freq=0
rel_freq=0
file_name_d=''
for i in range(0,length):
    can=0
    
    file_name='file'+str(i)
    with open('file%s.txt' % i, 'r') as words:
        abcd=words.read()
    words_list=abcd.split()
    size_list=len(words_list)
    for word in words_list:
        if word=='canada':
            can+=1
    if can!=0:
        table1.append_row([file_name,size_list,can])
    div=can/size_list
    if(div>rel_freq):
        rel_freq=div
        f_dict['rel_freq']=div
        f_dict['file_name_d']='file'+str(i)
        f_dict['word_freq']=can
    
    
f_list.append(f_dict)
print(table1)
print(f_list)
print("---------------------------3-----------------------------")
table2 = BeautifulTable()
table2.column_headers=['Document','Frequency','Relative Frequency']
for val in f_list:
    
    table2.append_row([val['file_name_d'],val['word_freq'],val['rel_freq']])
print(table2)



    
with open('output_part2.txt', 'w') as write_txt:
    write_txt.write("                                                                                \n")
    write_txt.write("                                                                                \n")
    write_txt.write("                                                                                \n")
    write_txt.write("-------------------------------------Question2--Part A--------------------------\n")
    write_txt.write("                                                                                \n")
    write_txt.write("Total Documents:"+str(length)+"\n")
    write_txt.write("                                                                                \n")
    write_txt.write("                                                                                \n")
    write_txt.write(str(table))
    write_txt.write("                                                                                \n")
    write_txt.write("                                                                                \n")
    write_txt.write("                                                                                \n")
    write_txt.write("-------------------------------------Question2--Part B--------------------------\n")
    write_txt.write("                                                                                \n")
    write_txt.write("Term: Canada\n")
    write_txt.write("                                                                                \n")
    write_txt.write("                                                                                \n")
    write_txt.write(str(table1))
    write_txt.write("                                                                                \n")
    write_txt.write("                                                                                \n")
    write_txt.write("                                                                                \n")
    write_txt.write("-------------------------------------Question2--Part C--------------------------\n")
    write_txt.write("                                                                                \n")
    write_txt.write("                                                                                \n")
    write_txt.write(str(table2))
    
'''
with open('news_finall.json','w') as news:
    json.dump(df,news)

'''








