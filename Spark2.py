from pyspark import SparkContext
from pyspark.sql import SQLContext, Row
import datetime

sc = SparkContext("spark://wolf.iems.northwestern.edu:7077")
sqlContext = SQLContext(sc)

data = sc.textFile("hdfs://wolf.iems.northwestern.edu:8020/user/huser69/crime/Crimes_-_2001_to_present.csv")
header = data.first()
rows = data.filter(lambda line: line != header)
parts = rows.map(lambda l: l.split(","))
def getDayofWeek(x):
    month = int(x[0:2])
    day = int(x[3:5])
    year = int(x[6:10])
    return(datetime.date(year,month,day).weekday())

def getWeek(x):
    month = int(x[0:2])
    day = int(x[3:5])
    year = int(x[6:10])
    return(datetime.date(year,month,day).isocalendar()[1])
def convertArrest(x):
    if x=="true":
        return(1)
    else:
        return(0)

crime_months = parts.map(lambda p: Row(arrest=(convertArrest(p[8])),crime=(1),month=(p[2][0:2]),year=(p[2][6:10]),day=(getDayofWeek(p[2])), \
    week=(getWeek(p[2]))))

schemaCrime = sqlContext.inferSchema(crime_months)
schemaCrime.registerTempTable("crimes")

query1 = sqlContext.sql("SELECT month, sum(arrest)/sum(crime) as Percent_Arrests FROM crimes GROUP BY month")
query1.rdd.saveAsTextFile("hdfs://wolf.iems.northwestern.edu:8020/user/huser69/crime/crimestoarrests")

query2 = sqlContext.sql("SELECT month, sum(arrest)/1620633 as Proportion_arrests from crimes group by month")
query2.rdd.saveAsTextFile("hdfs://wolf.iems.northwestern.edu:8020/user/huser69/crime/arrestsbymonth")

query3 = sqlContext.sql("Select day,sum(arrest)/1620633 as Proportion_arrests from crimes group by day")
query3.rdd.saveAsTextFile("hdfs://wolf.iems.northwestern.edu:8020/user/huser69/crime/dayofweek")
