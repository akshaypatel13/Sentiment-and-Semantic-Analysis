from pyspark.sql import SparkSession
from pyspark.sql import functions 
from operator import add

#  References
#		1. Sparksession and read data -- http://docs.mongodb.com/spark-connector/master/python-api/
#		2. Spark functions (explode, select, groupBy, isin, filter, union) -- https://spark.apache.org/docs/2.2.0/api/python/pyspark.sql.html#pyspark.sql.functions.when
#		3. convert tuples -- https://stackoverflow.com/questions/8366276/writing-a-list-of-tuples-to-a-text-file-in-python/8366338
#		4. Map reduce -- https://github.com/apache/spark/blob/master/examples/src/main/python/wordcount.py
#		5. Write to mongoDB from spark -- https://docs.mongodb.com/spark-connector/master/python/write-to-mongodb/


spark_mongo = SparkSession \
    .builder \
    .appName("DMW") \
    .config("spark.mongodb.output.uri", "mongodb://127.0.0.1/admin.word_count") \
    .getOrCreate()

tweets_mongo = spark_mongo.read.format("mongo").option("uri","mongodb://127.0.0.1/admin.tweets").load()
news_mongo = spark_mongo.read.format("mongo").option("uri","mongodb://127.0.0.1/admin.news").load()


tweets_fulltext=tweets_mongo.select('Tweet',functions.explode(functions.split('Tweet',' ')).alias('words_split_tweets'))
news_content=news_mongo.select('content',functions.explode(functions.split('content',' ')).alias('words_split_news'))
words_tweet = tweets_fulltext.select('words_split_tweets')
words_news = news_content.select('words_split_news')


keywords=['canada','university','education','dalhousie','faculty','computer science','graduate','expensive']
final_list_tweets=words_tweet.filter(words_tweet.words_split_tweets.isin(keywords))
final_list_news=words_news.filter(words_news.words_split_news.isin(keywords))
final=final_list_tweets.union(final_list_news)

tweets_ln = final.rdd.map(lambda r: r[0])
counts = tweets_ln.flatMap(lambda x: x.split(' '))  \
        .map(lambda x: (x, 1)) \
        .reduceByKey(add)
tweets_mapreduce = counts.collect()
count_mapreduce=spark.createDataFrame(tweets_mapreduce)


frequency_count_tweets=(final_list_tweets.groupBy(final_list_tweets.words_split_tweets).count())
frequency_count_news=(final_list_news.groupBy(final_list_news.words_split_news).count())
frequency_count=frequency_count_tweets.union(frequency_count_news)
keywords_negative=['poor school','poor schools','bad school','bad schools']
keywords_positive=['good school','good schools']

pos_list_tweets=tweets_mongo.filter(tweets_mongo.Tweet.isin(keywords_positive))
neg_list_tweets=tweets_mongo.filter(tweets_mongo.Tweet.isin(keywords_negative))

pos_list_news=news_mongo.filter(news_mongo.content.isin(keywords_positive))
neg_list_news=news_mongo.filter(news_mongo.content.isin(keywords_negative))

comp_count_tweets=tweets_mongo.filter(tweets_mongo.Tweet.contains('computer science'))
comp_count_news=news_mongo.filter(news_mongo.content.contains('computer science'))


space_tweets=spark.createDataFrame([('Positive Remarks Tweets',pos_list_tweets.count()),('Negative Remarks Tweets',neg_list_tweets.count()),('Computer Science Tweets',comp_count_tweets.count())],['words_split','count'])
space_news=spark.createDataFrame([('Positive Remarks',pos_list_news.count()),('Negative Remarks',neg_list_news.count()),('Computer Science',comp_count_news.count())],['words_split','count'])

space_freq=count_mapreduce.union(space_tweets)
words_count=space_freq.union(space_news)


combined_words_space=words_count.collect()
with open('map_reduce.txt','w') as file_output:
	for element in combined_words_space: 
		file_output.write(" ".join(map(str,element)))
		file_output.write("\n")

combined_words_space.write.format("mongo").mode("append").save()