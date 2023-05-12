# -*- coding: utf-8 -*-
"""
@author: Margarita
"""

# Initial setup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

# Setting the default resolution of plots to 300
plt.rcParams['figure.dpi'] = 300

# Reading data to be used in the regression
raw = pd.read_csv('db_reg.csv')

# Converting string variables in numeric variables
acres = raw["Acres"].to_list()
acres_list = []
for a in acres:
    a = a.split(",")
    a = "".join(a)
    acres_list.append(a)
    
d4 = raw["D4"].to_list()
d4_list = []
for d in d4:
    d = d.split(",")
    d = "".join(d)
    d4_list.append(d)

#%%

# Creating the dataframe of numerical variables with the year as index
db_file = pd.DataFrame({"Acres":acres_list,"D4":d4_list}, index=raw["Year"])
db_file[["Acres","D4"]] = db_file[["Acres","D4"]].astype(int)

# Converting the units of measurement into millions and thousands respectively
db_file["Acres"] = db_file["Acres"]/1e06
db_file["D4"] = db_file["D4"]/1e03

# Drawing the regresion line
# Creating a new single-panel figure
fig,ax1 = plt.subplots()
sns.regplot(data=db_file, x='D4', y='Acres', ax=ax1)
# Setting the title
ax1.set_title("Impact of exceptional drought on annual wildfire acres")
ax1.set_xlabel("Exceptional drought")
ax1.set_ylabel("Annual wildfire acres")
# Adjusting label spacing and axis
fig.tight_layout()
# Saving the figure
fig.savefig("reg_US.png")

#%%

# Defining the dependent variable 
dep_var  = 'Acres'
# Defining the independent variable
ind_vars = 'D4'

#  Setting things up for the statsmodels API
x = ind_vars
Y = db_file[dep_var]

X = db_file[ind_vars]
X = sm.add_constant(X)

model = sm.OLS(Y,X)

#%%
#  Doing the actual estimation and print a summary
results = model.fit()

print( results.summary() )