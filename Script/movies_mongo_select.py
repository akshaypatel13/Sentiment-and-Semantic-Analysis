from pyspark.sql import SparkSession
from pyspark.sql import functions 

# References
# 		1. Sparksession and read data -- http://docs.mongodb.com/spark-connector/master/python-api/
#		2. Spark functions (explode, select, groupBy, isin, filter, union) -- https://spark.apache.org/docs/2.2.0/api/python/pyspark.sql.html#pyspark.sql.functions.when
#		3. Write to mongoDB from spark -- https://docs.mongodb.com/spark-connector/master/python/write-to-mongodb/

spark = SparkSession \
    .builder \
    .appName("DMW") \
    .config("spark.mongodb.output.uri", "mongodb://127.0.0.1/admin.output_movies") \
    .getOrCreate()

movies_mongo = spark.read.format("mongo").option("uri","mongodb://127.0.0.1/admin.movies_f").load()

select_movies = movies_mongo.select('genre','ratings.value','plot')
final_movies = select_movies.collect()
with open('final_movies_1.txt','w') as file_output:
	for element in final_movies: 
		file_output.write(",".join(map(str,element)))
		file_output.write("\n")

select_movies.write.format("mongo").mode("append").save()
