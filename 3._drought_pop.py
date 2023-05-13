
# -*- coding: utf-8 -*-
"""
@author: Margarita
"""

# Initial setup
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

# Setting the default resolution of plots to 300
plt.rcParams['figure.dpi'] = 300
    
# Setting variable api to the American Community Survey 5-Year API endpoint for 2018
api = 'https://api.census.gov/data/2018/acs/acs5'

# Indicating what kind of geographic unit should be returned 
for_clause = 'county:*'
in_clause = 'state:*'

# Census API key
key_value = "3193647936b01a82a73830d81ce2413ad1fcd748"

# Build an HTTPS query string, send it to the API endpoint, and collect the response
payload = {'get':["B01001_001E"],'for':for_clause, 'in':in_clause,'key':key_value}
response = requests.get(api,payload)

# Testing if the request succeeded
if response.status_code == 200:
    print( "The request succeeded" )
else:
    print(response.status_code, response.text)
    assert False
    
# Parse the JSON returned by the Census server and return a list of rows
row_list = response.json()

# Converting the data into a Pandas dataframe
colnames = row_list[0]
datarows = row_list[1:]

pop = pd.DataFrame(columns=colnames,data=datarows)

# Renaming a column of the dataframe
pop = pop.rename(columns={"B01001_001E": "Population"})

# Converting numeric variable into string variable
pop['county'] = pop['county'].astype(str)

# Creating a new column (as a result of concatenating other two)
pop['FIPS'] = pop['state'] + pop['county']

# Write out the dataframe
pop.to_csv("pop_data.csv")


#%%

# Set up a dictionary to keep the FIPS elements of the list as strings 
fips_list = ["State","County","FIPS", "state","county"]
fips_cols = {col:str for col in fips_list}

# Reading the data
drought_data = pd.read_csv('dm_export_20230425_20230425 tot area by county.csv',dtype=fips_cols)
pop_data = pd.read_csv('pop_data.csv',dtype=fips_cols)

# Doing the left join of the population data onto the drought data 
drought_by_pop = drought_data.merge(pop_data, on='FIPS', how='left', validate='1:1', indicator=True)  ##See merge

# Printing the merge indicator 
print( drought_by_pop["_merge"].value_counts() )

# Dropping extra columns
drought_by_pop = drought_by_pop.drop(['_merge','Unnamed: 0', 'StatisticFormatID'], axis='columns')

# Sorting the data by FIPS code
drought_by_pop = drought_by_pop.sort_index()

#saving the data file to csv 
drought_by_pop.to_csv("Drought_by_population.csv")

#%%

# Dropping unnecesary columns
d4_by_pop = drought_by_pop.drop(columns=['None','D0', 'D1','D2', 'D3']) 

# Converting string variables to numerical variables
d4 = d4_by_pop["D4"].to_list()
d4_list = []
for d in d4:
    d = d.split(",")
    d = "".join(d)
    d4_list.append(d)

pop = d4_by_pop["Population"].to_list()

d4_by_pop = pd.DataFrame({"D4":d4_list,"Population":pop}, index=d4_by_pop["County"])
d4_by_pop["D4"] = d4_by_pop["D4"].astype(float)

# Filtering the data
d4_by_pop = d4_by_pop.query("D4 > 0")

# # Converting the units of population column (in millon) 
d4_by_pop["Population (mil)"] = d4_by_pop["Population"]/1e06

# Constructing the graph (a scatter plot)
d4_pop =sns.scatterplot(data = d4_by_pop, x = "D4", y = "Population (mil)")
# Setting the title
d4_pop.set_title("Exceptional drought by population in counties")
d4_pop.set_xlabel("Exceptional drought")
d4_pop.set_ylabel("Population (mil)")
# Saving the figure
plt.savefig("drought_pop_bycounties.png")

# Ranking the top 5 counties with the largest and smallest populations
d4_by_pop = d4_by_pop.sort_values(["Population"])
high_counties_pop = d4_by_pop[-5:]
low_counties_pop = d4_by_pop[:5]

# Ranking of the 5 counties with the highest and lowest areas of exceptional drought 
d4_by_pop = d4_by_pop.sort_values(["D4"])
high_counties_drought = d4_by_pop[-5:]
low_counties_drought = d4_by_pop[:5]


# Picking out the counties with highest populations 
top5_pop=d4_by_pop.sort_values(["Population (mil)"]).iloc[-5:]
print("\nTop 5 counties by population with exceptional drought in US:","\n",top5_pop)

# Picking out the counties with highest areas of exceptional drought 
top5_drought=d4_by_pop.sort_values("D4").iloc[-5:]
print("\nTop 5 counties with exceptional drought in US:","\n",top5_drought)


# Plotting the top 5 counties by population with exceptional drought
# Bulding a bargraph
fig, ax1= plt.subplots()
sns.barplot(x="D4", y="Population (mil)", data=top5_pop.reset_index(), ax=ax1)
plt.ylabel('Population')
plt.xlabel('Exceptional Drought')
plt.title('Top 5 counties by population with exceptional drought')
fig.savefig('top5_pop.png')

# Plotting the top 5 counties with the highest areas of exceptional drought
# Bulding a bargraph
fig, ax1= plt.subplots()
sns.barplot(x="D4", y="Population (mil)", data=top5_drought.reset_index(), ax=ax1)
plt.ylabel('Population')
plt.xlabel('Exceptional Drought')
plt.title('Top 5 counties with the highest areas of exceptional drought')
fig.savefig('top5_drought.png')

