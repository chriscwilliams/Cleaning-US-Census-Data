import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import codecademylib3_seaborn
import glob

# Importing files and creating a single dataframe with pd.concat
files = glob.glob('states*.csv')
dataframes = []
for filename in files:
  data = pd.read_csv(filename)
  dataframes.append(data)

us_census = pd.concat(dataframes)
# Creating a copy of the df to preserve the original data
census_data = us_census.copy()

# Removing the $ from the Income column data, converting the data to a float for easy manipulation, renaming the column to be more descriptive as well and rounding the data to 2 decimals since we are using dollar values

census_data['Income'] = census_data['Income'].apply(lambda x: x.replace('$', ''))
census_data['Income'] = pd.to_numeric(census_data['Income'])
census_data['Income'] = census_data['Income'].round(2)
census_data = census_data.rename(columns={'Income': 'Income ($)'})


# Delete the column named 'unnamed: 0', drop duplicated columns and reset the index
# Because I will be dropping columns I will save the results to new variables

census_data_edited = census_data.drop(columns='Unnamed: 0').reset_index()
census_data_edited_2 = census_data_edited.drop(columns='index')

# GenderPop column split into a series with each row being a list of male data at the 0 index and female data at the 1 index
split_genderpop = census_data_edited_2['GenderPop'].str.split('_')

census_data_edited_2['Male Population'] = split_genderpop.str[0]
census_data_edited_2['Female Population'] = split_genderpop.str[1]

census_data_edited_3 = census_data_edited_2.drop(columns='GenderPop')

# Remove the M and F from the gender population columns

census_data_edited_3['Male Population'] = census_data_edited_3['Male Population'].apply(lambda x: x.replace('M', ''))
census_data_edited_3['Female Population'] = census_data_edited_3['Female Population'].apply(lambda x: x.replace('F', ''))

# Convert the the string columns to ints
census_data_edited_3['Male Population'] = pd.to_numeric(census_data_edited_3['Male Population'])
census_data_edited_3['Female Population'] = pd.to_numeric(census_data_edited_3['Female Population'])

# Drop duplicate rows

census_data_edited_4 = census_data_edited_3.drop_duplicates().reset_index().drop(columns='index')

# Filling NaN values
census_data_edited_5 = census_data_edited_4.fillna(value={
  'Female Population': census_data_edited_4['TotalPop'] - census_data_edited_4['Male Population']
})

# View Dataframe
plt.scatter(census_data_edited_5['Female Population'], census_data_edited_5['Income ($)'])
plt.xlabel('Female Population')
plt.ylabel('Income $')
plt.title('Female Population vs Income')
plt.show()
plt.cla()

data = census_data_edited_5.copy()


# Removing % sign from Demographic columns
data.Hispanic = data.Hispanic.str[:-1]
data.White = data.White.str[:-1]
data.Black = data.Black.str[:-1]
data.Native = data.Native.str[:-1]
data.Asian = data.Asian.str[:-1]
data.Pacific = data.Pacific.str[:-1]

# Converting Demographic columns to numerical and rounding to 2 decimals
data.Hispanic = pd.to_numeric(data.Hispanic).round(2)
data.White = pd.to_numeric(data.White).round(2)
data.Black = pd.to_numeric(data.Black).round(2)
data.Native = pd.to_numeric(data.Native).round(2)
data.Asian = pd.to_numeric(data.Asian).round(2)
data.Pacific = pd.to_numeric(data.Pacific).round(2)

# Fill NaN values in Pacific column
data = data.fillna(value={
  'Pacific': (100 - (data.Hispanic + data.White + data.Black + data.Native + data.Asian)).round(2)
})

# Histogram for each dempgraphic column

plt.hist(data.Hispanic)
plt.title('Hispanic Population')
plt.xlabel('Percentage')
plt.ylabel('Frequency of occurence')
plt.show()
plt.cla()

plt.hist(data.White)
plt.title('White Population')
plt.xlabel('Percentage')
plt.ylabel('Frequency of occurence')
plt.show()
plt.cla()

plt.hist(data.Black)
plt.title('Black Population')
plt.xlabel('Percentage')
plt.ylabel('Frequency of occurence')
plt.show()
plt.cla()

plt.hist(data.Asian)
plt.title('Asian Population')
plt.xlabel('Percentage')
plt.ylabel('Frequency of occurence')
plt.show()
plt.cla()

plt.hist(data.Native)
plt.title('Native Population')
plt.xlabel('Percentage')
plt.ylabel('Frequency of occurence')
plt.show()
plt.cla()

plt.hist(data.Pacific)
plt.title('Pacific Population')
plt.xlabel('Percentage')
plt.ylabel('Frequency of occurence')
plt.show()
plt.cla()

# View dataframe
print(data.head(51))