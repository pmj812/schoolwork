from pyspark import SparkContext
from pyspark.mllib.stat import Statistics
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint, LinearRegressionWithSGD
import numpy as np
import datetime
import math

sc = SparkContext("spark://wolf.iems.northwestern.edu:7077")
data = sc.textFile("hdfs://wolf.iems.northwestern.edu:8020/user/huser69/crime/Crimes_-_2001_to_present.csv")
header = data.first()
rows = data.filter(lambda line: line != header)
parts = rows.map(lambda l: l.split(","))
parts = parts.persist()

def getWeek(x):
    month = int(x[0:2])
    day = int(x[3:5])
    year = int(x[6:10])
    return(datetime.date(year,month,day).isocalendar()[1])

violent = ["ASSAULT","BATTERY","CRIM SEXUAL ASSAULT", "DOMESTIC VIOLENCE", "HOMICIDE", "KIDNAPPING"]
def setFlags(x):
        if x in violent:
                return (0,1)
        else:
                return (1,0)

beats = parts.map(lambda p:(p[10],p[2][6:10],getWeek(p[2]),1,setFlags(p[5])))
beats2 = beats.filter(lambda x:x[1]=="2015").map(lambda x:((x[0],x[2]),(x[3],x[4][0],x[4][1])))
beats3 = beats2.reduceByKey(lambda x,y: (x[0]+y[0],x[1]+y[1],x[2]+y[2]))
standard_vars = beats3.map(lambda row: Vectors.dense((row[0][1],row[1][0],row[1][1],row[1][2])))
summary = Statistics.colStats(standard_vars)
mean_wn = summary.mean()[0]
sd_wn = math.sqrt(summary.variance()[0])
mean_counts = list(summary.mean()[1:4])
sd_counts = list(np.sqrt(summary.variance()[1:4]))
beats_standard = beats3.map(lambda x: (x[0][0],(x[0][1]-mean_wn)/(sd_wn),(x[1][0]-mean_counts[0])/sd_counts[0],(x[1][1]-mean_counts[1])/sd_counts[1], \
 (x[1][2]-mean_counts[2])/sd_counts[2]))
beats_list = beats_standard.map(lambda x: ((x[0]),1)).keys().distinct().collect()
beats_list = beats_list[0:50]
def parsePoint(tuple):
        values = [float(x) for x in tuple]
        return LabeledPoint(values[0], values[1:])
def deNorm(val,mean,sd):
        return(val*sd + mean)
maxWeek = (21 - mean_wn) / sd_wn
curWeek = (20 - mean_wn) / sd_wn
predictions = {}
beats_standard  = beats_standard.persist()
for beat in beats_list:
    curr_beat = beats_standard.filter( lambda x: x[0]==beat and x[1] <= curWeek )
    next_beat = beats_standard.filter( lambda x: x[0]==beat and x[1] == maxWeek )
    if not next_beat.take(1):
            next_beat = beats_standard.filter( lambda x: x[0]==beat and x[1] == curWeek )
    labeled_beats1 = curr_beat.map(lambda x: parsePoint((x[3],x[1])))
    labeled_beats2 = curr_beat.map(lambda x: parsePoint((x[4],x[1])))
    fit_beats1 = LinearRegressionWithSGD.train(labeled_beats1)
    fit_beats2 = LinearRegressionWithSGD.train(labeled_beats2)
    labeled_beats1 = next_beat.map(lambda x: parsePoint((x[3],x[1])))
    labeled_beats2 = next_beat.map(lambda x: parsePoint((x[4],x[1])))
    valuesAndPreds1 = labeled_beats1.map(lambda p: (deNorm(p.label,mean_counts[1],sd_counts[1]), deNorm(fit_beats1.predict(p.features),mean_counts[1],sd_counts[1])))
    valuesAndPreds1Vals = valuesAndPreds1.collect()
    valuesAndPreds1Array = np.array(valuesAndPreds1Vals[0])
 valuesAndPreds2 = labeled_beats2.map(lambda p: (deNorm(p.label,mean_counts[2],sd_counts[2]), deNorm(fit_beats2.predict(p.features),mean_counts[2],sd_counts[2])))
    valuesAndPreds2Vals = valuesAndPreds2.collect()
    valuesAndPreds2Array = np.array(valuesAndPreds2Vals[0])
    finalPredictions = valuesAndPreds1Array + valuesAndPreds2Array
    predictions[beat] = finalPredictions
sum = 0
for beat, crime in predictions.iteritems():
        sum+=(crime[0] - crime[1])**2

print(predictions)
print(sum / len(beats_list))

