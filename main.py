import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

#Read csv File with raw data

myData= pd.read_csv("rfm_data.csv")

#Remove duplicates by making a copy of original Data
data = myData.copy(deep=True).drop_duplicates(subset=["CustomerID"],keep="last")


#Calculate frequency of each CustomerID
frequencySeries =myData.CustomerID.value_counts().reset_index(name="Frequency")
# print(frequencySeries.loc[frequencySeries["CustomerID"]==8317])



#Appending frequency column to DataFrame
frequencySeries.rename({"index":"CustomerID"},inplace=True)
data = data.merge(frequencySeries,on="CustomerID",how="left")


#Total Money spent per user
moneySpent = myData.groupby("CustomerID")['TransactionAmount'].sum().reset_index(name="Total Spent")
data= data.merge(moneySpent,on="CustomerID",how="left")




recencyScore = [5,4,3,2,1,]
frequencyScore = [1,2,3,4,5]
monetaryScore = [1,2,3,4,5]

#Grading users 
data["recencyScore"] =pd.cut(data["recency"],bins=5,labels=recencyScore).astype(int)

data["FrequencyScore"] = pd.cut(data["Frequency"],bins=5,labels=frequencyScore).astype(int)

data["Monetary Score"] = pd.cut(data["Total Spent"],bins=5,labels=monetaryScore).astype(int)

data['totalScore'] = data["FrequencyScore"] + data["Monetary Score"] + data["recencyScore"]

#Ranking users based on ttal RFM score

myLabels = ["Beginner","Intermediate","PRO"]
data["Rank"] = pd.cut(data["totalScore"],bins=3,labels=myLabels)



#extracting values to plot

typeBeginners = data.loc[data["Rank"]=="Beginner"]
typeInter = data.loc[data["Rank"]=="Intermediate"]
typePro= data.loc[data["Rank"]=="PRO"]

beginners = typeBeginners.mean(numeric_only=True)["Total Spent"]

intermediate = typeInter.mean(numeric_only=True)["Total Spent"]

pro = typePro.mean(numeric_only=True)["Total Spent"]

# print(len(data.loc[data["Rank"]=="Intermediate"]))


# print(tokyoBeg)

#Arry with locations
locations = data["Location"].drop_duplicates().values
#print(locations)

#Tokyo = data.loc[data["Location"] == "Tokyo"]

'''
plt.pie([len(typeBeginners),len(typeInter),len(typePro)],labels=myLabels,autopct='%1.1f%%')
plt.axis('equal')
plt.legend(labels=myLabels)
plt.show()'''
locationLabels = ['Tokyo' ,'London', 'New York', 'Paris']
def getType(myType,myCity) :
    return len(data.loc[(data["Rank"]==myType) & (data["Location"]==myCity)])


    

# myCityStats = {
#     "Beginners":[getType("Beginner",i) for i in locationLabels],
#     "Intermediate":[getType("Intermediate",j) for j in locationLabels],
#     "PRO": [getType("PRO",k)for k in locationLabels]
# }
myCityStats={}
for i in myLabels:
    for j in locationLabels:
        myCityStats[i]= [getType(i,j) for j in locationLabels]
        
print(myCityStats)

x=np.arange(len(locationLabels))
width = 0.3
multiplier = 0

fig,ax = plt.subplots(layout='constrained')

for att,val in myCityStats.items():
    offset = width*multiplier
    bars = ax.bar(x+offset,val,width,label=att)
    ax.bar_label(bars,padding=3)
    multiplier+=1
    

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Length (mm)')
ax.set_title('Number of users in a city per RFM Rank')
ax.set_xticks(x + width, locationLabels)
ax.legend(loc='upper left', ncols=3)
ax.set_ylim(0, 250)

plt.show()







    
    
    





 

# print(frequencySeries)