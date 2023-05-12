# -*- coding: utf-8 -*-
"""
@author: Margarita
"""

# A. Initial setup
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns


# Setting the default resolution of plots to 300
plt.rcParams['figure.dpi'] = 300

# Set up a dictionary to keep the FIPS elements of the list as strings 
fips_list = ["STATEFP","COUNTYFP","GEOID", "state","county"]
fips_cols = {col:str for col in fips_list}

# Reading the data
geo_data = pd.read_csv('county_geo.csv',dtype=fips_cols)
pop_data = pd.read_csv('county_pop.csv',dtype=fips_cols)

# Doing the left join of pop_data onto geo_data using the state and county FIPS codes
merged = geo_data.merge(pop_data, left_on=["STATEFP","COUNTYFP"], right_on=["state","county"],how="left")

# Setting the index to the State and County FIPS codes
merged = merged.set_index(["STATEFP","COUNTYFP"])

# Renaming the column of population
merged = merged.rename(columns={'B01001_001E':'pop'})

# Convert square meters to square miles
merged['sq_miles'] = merged['ALAND']/2.59e6

# Calculate the density of population's column
merged['density'] = merged['pop']/merged['sq_miles']

# Converting the units of population column (in millon) 
merged['pop_mil'] = merged['pop']/1e6

# Renaming a column
merged = merged.rename(columns={"GEOID":"FIPS"})

# Coververting into numbers
merged["FIPS"] = merged["FIPS"].astype(float)

# Sorting the data by FIPS code
merged = merged.sort_index()

# Writing the data out to a file
merged.to_csv('county_merged.csv')

#%%
# Reading the drought data
sh_drought_data = pd.read_csv('dm_export_20230425_20230425 tot area by county.csv',dtype=fips_cols)

# Doing the left join of county data onto drought data 
sh_drought_by_pop = sh_drought_data.merge(merged, on='FIPS', how='left', validate='1:1', indicator=True)  

# # Printing the merge indicator
print( sh_drought_by_pop["_merge"].value_counts() )

# Dropping extra columns
sh_drought_by_pop = sh_drought_by_pop.drop(['_merge','StatisticFormatID'], axis='columns')

# Sorting the data by FIPS code
sh_drought_by_pop = sh_drought_by_pop.sort_index()

# Writing out the datafile 
sh_drought_by_pop.to_csv("Sh_drought_by_population.csv")

#%%
# Converting string variables to numerical variables
d2 = sh_drought_by_pop["D2"].to_list()
d2_list = []
for d in d2:
    d = d.split(",")
    d = "".join(d)
    d2_list.append(d)
    
d3 = sh_drought_by_pop["D3"].to_list()
d3_list = []
for d in d3:
    d = d.split(",")
    d = "".join(d)
    d3_list.append(d)
    
d4 = sh_drought_by_pop["D4"].to_list()
d4_list = []
for d in d4:
    d = d.split(",")
    d = "".join(d)
    d4_list.append(d)

sqm = sh_drought_by_pop["sq_miles"].to_list()
pop = sh_drought_by_pop["pop_mil"].to_list()

# Creating a new dataframe with County as the index
trim = pd.DataFrame({"D2":d2_list,"D3":d3_list,"D4":d4_list,"sq_miles":sqm,"pop_mil":pop}, index=sh_drought_by_pop["County"])

trim[["D2", "D3", "D4"]] = trim[["D2", "D3", "D4"]].astype(float)

# Dataframe with the shares of drought areas and population at county level
share = trim.div(trim["sq_miles"], axis='index')

# Sum of drought area shares
tot_sh = share["D2"] + share["D3"] + share["D4"]

# Population in the share of drought areas
tot_sh_pop = tot_sh*pop

# Dataframe with the variables to be plotted
share_pop = pd.DataFrame({"total_share":tot_sh,"total_share_pop":tot_sh_pop})
share_pop = share_pop.query("total_share<=1")

# Constructing the figure (a scatter plot)
share_pop =sns.scatterplot(data=share_pop, x = "total_share", y = "total_share_pop")
share_pop.set_title("Exceptional drought by population in counties")
plt.savefig("sh_drought_pop_bycounties.png")
