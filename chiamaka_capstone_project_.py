# -*- coding: utf-8 -*-
"""Chiamaka Capstone Project .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1nH-FzxJ4ZK6omwDJX2YHnqxUq71XCl8D

**NAME: FRANCIS CHIAMAKA ETHEL**

The aim of this project is to study the dataset gotten from several restaurants around the world to get insight on a number of variables like their cuisines, the city in which they are located, how much customers love the dishes they purchase from these restaurants, the nature of service these restaurants offer and how well customers rate them.
At the end of this study a predictive model would be done to predict how much customers are delighted in particular restaurants and what they offer

# **WEEK 1: DATA EXPLORATION**
1.   Dataset Overview
2.   Analysing aggregate rating: Checking for imbalances
3.   Calculating statistics for numerical columns; exploring categorical columns and checking for top 5 cuisines and cities.
"""

# Importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('https://github.com/Oyeniran20/axia_class_cohort_7/raw/refs/heads/main/Dataset%20.csv')

"""# **Dataset Overview**"""

df.head(5)

df.shape

"""The data set contains 9551 rows and 21 columns"""

df.info()

#checking for missing values
df.isnull().sum().sort_values(ascending=False)

missing_values = df.isnull().mean()*100
missing_values.sort_values(ascending=False)

"""Due to the fact that having missing values can affect our prediction, it was necessary to find out the amount of missing value and its percentage. In the cuisine column I discovered that there are 9 rows without inputed data. This gives me an insight as to how I deal with my data so I don't have a model that predicts in a biased way.
Cuisine column is not dropped despite having missing data because of its importance
"""

# Checking Duplicate Data
df.duplicated().sum()

"""**Checking for Incorrect Values in the Data Set and Replacing Them**"""

df['Restaurant Name']

import re

df['Restaurant Name'] = df['Restaurant Name'].apply(lambda x: re.sub(r'[^\w\s]', ' ', x))

df['Restaurant Name']

df['City']

df['City'] = (
    df.City.str.extract(r'([a-zA-Z\s]+)')
)

df['City']

df['City'] = df['City'].replace('stanbul','Istanbul')

df['City']

df['Address']

df['Address'] = df['Address'].apply(lambda x: re.sub(r'[^\w\s]', '', x))

df['Address']

df['Locality']

df['Locality'] = df['Locality'].apply(lambda x: re.sub(r'[^\w\s]', '', x))

df['Locality']

df['Locality Verbose']

df['Locality Verbose'] = df['Locality Verbose'].apply(lambda x: re.sub(r'[^\w\s]', '', x))

df['Locality Verbose']

df['Locality Verbose'].unique()

df['Locality Verbose'] = df['Locality Verbose'].replace({'Kuru_eme stanbul':'Kuru_eme Istanbul', 'Karak_y stanbul':'Karak_y Istanbul', 'Kouyolu stanbul':'Kouyolu Istanbul', 'Moda stanbul' : 'Moda Istanbul' })

df['Locality Verbose']

df['Cuisines'].unique()

df['Currency']

# dropping rows where cuisine is empty
df = df.dropna(subset=['Cuisines'])

"""**I dropped the rows with missing cuisines to avoid errors in prediction since the cuisine column is important to my machine learning process**"""

df.head(3)

"""While exploring the data set I observed that there were special characters in the names found in the following columns: Restaurant name, City, Address, Locality and Locality verbose; which are not supposed to be there. I went through the process of cleaning them out, replacing misspelt names with the correct names. All of this was done to make the data set presentable in preparation for machine learning processes."""

df.shape

"""The size of the dataset has reduced by 9 values due to the dropping of the missing value rows in the cuisine value

# **Analysing aggregate rating**
"""

# checking for ouliers in numerrical columns
# Histogram and Box plot of aggregate rating
plt.figure(figsize=(8, 6))
plt.subplot(1, 2, 1)
sns.histplot(df['Aggregate rating'], bins=20, kde=True)
plt.title('Histogram of Aggregate Rating')
plt.xlabel('Aggregate Rating')
plt.ylabel('Frequency')

plt.subplot(1, 2, 2)
sns.boxplot(df['Aggregate rating'])
plt.title('Box Plot of Aggregate Rating')
plt.ylabel('Aggregate Rating')

plt.show()

"""**From the visualization it is observed that the number of 0.0 rating is extremely high which shows that customers were not satisfied with either the goods or services gotten from the restaurants or even both**"""

df['Aggregate rating']

df['Aggregate rating'].max()

df['Aggregate rating'].min()

"""# **Descriptive Analysis**"""

df.describe().T

"""The dataset description shows us the statistical informations about our numerical columns, where the exponential factor(e) represents . Informations such as the mean, standard deviation, minimum values, average values(50%) and maximum values are shown in the table"""

# Exploration of Categorical Variables
df['Cuisines'].value_counts()

"""**The top five cuisines are: North Indian; North Indian, Chinese; Chinese; Fast food and North Indian, Mughlai**"""

df['City'].value_counts()

"""**The top five cities are New Delhi, Gurgoan, Noida, Faridabad, Ghaziabad**

# **WEEK 2: DATA VISUALIZATION**
1.   Visualizations
2.   Geospatial analysis
3.   Additional analysis

# Visualization

To see the relationships between different variables, visualization is used.
"""

!pip install plotly

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# numerical and categorical columns
num_cols = df.select_dtypes(include=np.number).columns
cat_cols = df.select_dtypes(include=['object']).columns

num_cols

cat_cols

# visualizing
for col in num_cols:
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    sns.histplot(df[col], bins=20, kde=True)
    plt.title(f'Histogram of {col}')
    plt.xlabel(col)
    plt.ylabel('Frequency')

    #Boxplot
    plt.subplot(1, 2, 2)
    sns.boxplot(x=df[col], color='green')
    plt.title(f'{col} Boxplot')
    plt.xlabel(col)

    plt.show()

"""From the visualization, it can be observed that there are outliers in Country code, Longitude, Latitude, Averagecost for two, Price range, Aggregate rating and Votes.

These outliers need to be resolved to ensure that the prediction is accurate and precise

**Checking for the number of zeros in the columns with outliers to enable me know how to deal with them**
"""

zeros_agg=len(df[df['Aggregate rating'] == 0])

zeros_agg

"""There are 2148 rows in the aggregate rating column that 0.0 rating. The inference I can take from this observation is that the customers probably did not like or appreciate anything about the restaurants and therefore did not rate them."""

zeros_code=len(df[df['Country Code'] == 0])

zeros_code

"""There are no rows with 0 input in the country code column."""

zeros_lng=len(df[df['Longitude'] == 0])

zeros_lng

zeros_lat=len(df[df['Latitude'] == 0])

zeros_lat

"""For the longitude and latitude column 498 rows were observed to contain 0 inputs."""

zeros_cost=len(df[df['Average Cost for two'] == 0])

zeros_cost

"""15 rows contain 0 in the average cost for two column"""

zeros_price=len(df[df['Price range'] == 0])

zeros_price

"""There are no 0 found in the price range column"""

zeros_votes=len(df[df['Votes'] == 0])

zeros_votes

"""There are 1094 rows which contain 0 in the Votes column."""

rating_view = df[['Aggregate rating', 'Rating text', 'Votes', 'Rating color']]
rating_view.sample(7)

"""During my analysis of the ratings and votes, i observed that some vote columns had values greater than 0 but their aggregate ratings had 0 values. That made me look into it and i observed that the aggregate ratings were gotten by using the ratings gotten from each individual (from 1 to 5) against the votes and solved mathematically. Due to this fact it can be seen that some restaurants that had much more votes that some others had lesser aggregate ratings as the indivual ratings were'nt good enough- falling into lower ranges of 1 to 3.
This is a factor to the skewness that was observed in visualization where we have individual ratings as low as 1 or 2.

**Filling up rows in latitude and longitude columns with 0 with the mean of similar areas**
"""

import pandas as pd

# Group data by city and get the mean latitude and longitude for each city
city_coords = df.groupby('City')[['Latitude', 'Longitude']].mean().reset_index()

# Create a dictionary mapping cities to their coordinates
city_coords_dict = dict(zip(city_coords['City'], zip(city_coords['Latitude'], city_coords['Longitude'])))

# Fill in coordinates with 0 using the dictionary
for index, row in df.iterrows():
    if row['Latitude'] == 0 or row['Longitude'] == 0:
        city = row['City']
        if city in city_coords_dict:
            df.loc[index, ['Latitude', 'Longitude']] = city_coords_dict[city]

zeros_count = len(df[df['Longitude'] == 0])

zeros_count

"""Geocoders are tools that convert textual location descriptions such as address, postal codes etc., to geographic coordinates(Longitude and Latitude) and vice versa. They can also be used in for the imputation.
Seeing that a number of the rows in my latitude and longitude columns were containing 0 which are the values of the Prime Meridian on the longitude and the Equator on the latitude. I had to look for a way to input the correct latitude and longitude values.

This would enable me get a good geospatial representation.

**Outliers and their effects**

*   In the longitude and latitude columns i noticed a couple of 0's which are abnormal as no real place actually has those coordinates. While this may not be the entire reason for the outliers, I ensured I took care of them.
*   The country code visualization showed the existence of large number of outliers. After going through the the dataset, I observed that the codes ranged from 1 to numbers greater than 100 which caused the skewed visualization. Since these country codes are actual in real life i.e they represent actual places, take for instance we have countries such as USA, Canada using the +1,it's effect on the visualization can be ignored.
*   The average rating column contains lots of zeros. This implies that several customers did not rate the services of these restaurants as ratings start from 1 and ends at 5, with 1 being very poor and 5 being excellent.
*   The average cost was observed to contain 0's whereas the cost for a product or service can never be 0 of whatever currency being used. This should be a misinputation and would be looked into later on.

**Visulaizing relationship between votes and ratings**
"""

plt.figure(figsize=(8, 6))
sns.scatterplot(x='Aggregate rating', y='Votes', data=df)
plt.title('Average Rating vs. Votes')
plt.xlabel('Average Rating')
plt.ylabel('Votes')
plt.show()

"""From my scatter plot I observed that there is a strong correlation between the average ratings and votes. The restaurants with the highest average ratings were observed to have a greater number of votes leading to the positive correlation. A few number of restaurants got high number of votes as most restaurants had relatively small number of votes. This is as a result of the visibility of these restaurants as these votes were based on how popular the restaurants were among customers.
The clusters show that there were a good number of restaurants with similar ratings

The higher the votes, the higher the ratings.

Using of a visualization tool called violin
"""

fig = px.violin(df, x="Aggregate rating", y="Votes")

fig.show()

"""# Comparing average ratings across cuisines and cities.

**Distribution for aggregate rating by Cuisine**
"""

avg_rating_by_cuisine = df.groupby('Cuisines')['Aggregate rating'].mean().reset_index()
fig = px.bar(avg_rating_by_cuisine,  y='Aggregate rating',x='Cuisines',
             title='Average Rating by Cuisine', color_discrete_sequence=['green'])

# customizing layout
fig.update_layout(yaxis_title='Average Rating',xaxis_title='Cuisine', plot_bgcolor='lightblue', xaxis={'categoryorder':'total descending'})

fig.show()

"""**Distribution for aggregate rating by City**"""

avg_rating_by_city = df.groupby('City')['Aggregate rating'].mean().reset_index()
fig = px.bar(avg_rating_by_city, x='City', y='Aggregate rating',
             title='Average Rating by City', color_discrete_sequence=['green'])

# customizing layout
fig.update_layout(xaxis_title='City', yaxis_title='Average aggregate Rating', plot_bgcolor='gray', xaxis={'categoryorder':'total descending'})

fig.show()

"""Using Pie chart to represent votes per city"""

# selecting top 10 city vote counts
city_votes = df['City'].value_counts().head(10).reset_index()
city_votes.columns = ['City', 'Votes']

# Creating pie chart
fig = px.pie(city_votes, values='Votes', names='City', title='Vote Percentage by City')

fig.show()

"""**From the pie chart it can be observed majority of the votes cames from New Delhi city**

# Geospatial Analysis
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import plotly.express as px

# For dataframe 'df' with 'Latitude', 'Longitude', 'City', and 'Restaurant Name' columns

# Creating geodata frame for mapping locations
fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", hover_name="Restaurant Name", hover_data=["City", "Cuisines"],
                        color_discrete_sequence=["darkorange"], zoom=3, height=600)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

"""The map is an 'Open street map'. An open street map is a map that includes data about roads, buildings, addresses, shops and businesses, points of interest, land use and natural features and much more.

It includes features such as hover name which is the restaurant name, hover data which includes the city names and the cuisines offered by the restaurant. For the margin layout, r = right side, t = top, l = left side, b = bottom. The margin layout was used to adjust the different sides removing any spaces around the map
"""

import plotly.express as px

city = df['City'].value_counts().head(30)
fig = px.bar(city, x=city.index, y=city.values, title="Number of Restaurants in Each City (Top 30)",
             color=city.values, color_continuous_scale="Plasma", text=city.values
            )

fig.update_layout(
    xaxis_title="City",
    yaxis_title="Number of Restaurants",
    xaxis={'categoryorder':'total descending'},
    plot_bgcolor='rgba(0,0,0,0)',  # Sets plot background to transparent
    xaxis_tickangle=-45,
    font=dict(family="Arial", size=12, color="black")  # Customize font style
)

fig.update_traces(texttemplate='%{text}', textposition='outside')  # Position text labels outside bars

fig.show()

"""Correlating location[Longitude and Latitude] with rating"""

sns.heatmap(df[['Latitude', 'Longitude', 'Aggregate rating']].corr(), annot=True, fmt='.2f', cmap= 'coolwarm')
plt.show()

"""From this correlation heat map it can be seen that there is a weak correlation or relationship between latitude and aggregate rating hence the -0.13 and as longitude tends to increase aggregate rating reduces explaining the negative correlation value. This could be as a result of the skewness in the aggregate rating column. Later on, if transformation is done we will see if there will be a difference in the the correlation heat map.

# **WEEK 3: CUSTOMER PEFERENCES**

1.   Cuisine Analysis
2.   Price Range
3.   Service Features

## Identifying highest rated cuisines
"""

cuisine_ratings = df.groupby('Cuisines')['Aggregate rating'].mean().reset_index()

highest_rated_cuisines = cuisine_ratings.sort_values(by=['Aggregate rating'], ascending=False)

highest_rated_cuisines.head(20)

"""The highest rating for a cuisine is 4.90 and there were 18 cuisines with this rating. It shows that so many customers preferred these cuisines and therefore they were rated highly.

## Comparing ratings across price points
"""

avg_rating_by_city = df.groupby('Price range')['Aggregate rating'].mean().reset_index()
fig = px.bar(avg_rating_by_city, x='Price range', y='Aggregate rating',
             title='Average Rating by Price range', color_discrete_sequence=['green'])

# customizing layout
fig.update_layout(xaxis_title='Price range', yaxis_title='Average aggregate Rating', plot_bgcolor='gray', xaxis={'categoryorder':'total descending'})

fig.show()

"""Price range 4 receives the highest rating.

## Identifying highest rated cuisines
"""

# selecting top 20 cuisines vote counts
city_votes = df['Cuisines'].value_counts().head(20).reset_index()
city_votes.columns = ['Cuisines', 'Votes']

# Creating pie chart
fig = px.pie(city_votes, values='Votes', names='Cuisines', title='Vote Percentage by Cuisines')

fig.show()

"""Using pie chart I have been able to show the top 20 highest rated cuisines. The highest voted cuisine is the North Indian cuisine with 936 votes; North India, Chinese cuisne was the second highest with 511 votes.

## Analysing Table Booking and Delivery
"""

df['Has Table booking']

df['Has Table booking'].value_counts()['Yes']

df['Has Table booking'].value_counts()['No']

"""The amount of restaurants that do not offer table booking is 8384 that is 87.86% while those that offer table booking is 1158 i.e, 12.14%."""

Booking_Delivery = df[['Has Table booking', 'Has Online delivery', 'Is delivering now']]

Booking_Delivery.sample(5)

sns.countplot(x='Has Table booking', data=df)
plt.title('Frequency of Table Booking')
plt.show()

sns.countplot(x='Has Online delivery', data=df)
plt.title('Frequency of Online delivery')
plt.show()

sns.countplot(x='Is delivering now', data=df)
plt.title('Frequency of Is delivering now')
plt.show()

"""From the table and visualization, it can be seen that most restaurants do not  have table booking and online delivery. The relationship between these two columns may differ. Where table booking may be 'yes' online delivery may be 'no'. There are also situations where both columns contain the same value."""

import seaborn as sns
import matplotlib.pyplot as plt

sns.boxplot(x='Has Table booking', y='Aggregate rating', data=df)
plt.title('Aggregate Rating Distribution by Table Booking')
plt.show()

table_booking_comparison = df[['Has Table booking', 'Aggregate rating']]

table_booking_comparison.sample(5)

"""It can be observed from this table that there is a relationship between 'Has table booking' and 'Aggregate Rating'. The restaurants without table booking tend to have lower ratings, while this might not be the cause it is observed that there is a correlation between them. While when the restaurants offer table booking the average rating is high.

**Online Delivery Analysis**
"""

# Checking for restaurants offering delivery.
df['Has Online delivery'].value_counts()

#Checking the percentage of restaurants offering delivery
delivery_count = df['Has Online delivery'].value_counts()['Yes']
total_restaurants = len(df)
delivery_percentage = (delivery_count / total_restaurants) * 100

delivery_percentage

"""The percentage of restaurants offering online delivery is 25.68% which is less than 50% of the number of restaurants"""

Delivery_Range_Comparism = df[['Has Online delivery', 'Price range']]

Delivery_Range_Comparism.sample(5)

"""From this table it can be said that the price range does not determine if the restaurant offers online delivery or not."""

# Example: Analyzing cuisine preferences by city
city_cuisine_ratings = df.groupby(['City', 'Cuisines'])['Aggregate rating'].mean().reset_index()

city_cuisine_ratings.sample(5)

"""Some cuisines are rated more highly than the others in different cities.

Checking for the highest rated cuisines in New Delhi.
"""

#Finding top cuisines in New Delhi
new_delhi_preferences = city_cuisine_ratings[city_cuisine_ratings['City'] == 'New Delhi']

new_delhi_preferences

"""# Predictive Modelling

1.   Feature Engineering
2.   Model Building
3.   Model Evaluation

### Feature Enginnering
"""

df['Price range'].max()

df['Price Category'] = pd.cut(
    df['Price range'],
    bins=[0,1, 2, 3, 4],
    labels = ['Budget Friendly', 'Mid Range', 'Expensive', 'Luxury Dining']
)

df['Cuisine Count'] = df['Cuisines'].apply(lambda x: len(x.split(',')))

df.sample(2)

# numerical and categorical columns
num_cols = df.select_dtypes(include = np.number).columns
cat_cols = df.select_dtypes(['object']).columns

num_cols

cat_cols

# Correlation of numerical columns
corr_matrix = df[num_cols].corr()
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm')
plt.show()

"""**Data Splitting**"""

X = df.drop(columns = ['Aggregate rating'])
Y = df['Aggregate rating']

X

Y

from sklearn.model_selection import train_test_split
train_inputs, test_input, train_targets, test_target = train_test_split(X, Y, test_size=0.2, random_state=42)

"""**Data Preprocessing**"""

from sklearn.preprocessing import OneHotEncoder, StandardScaler
encoder = OneHotEncoder(drop = 'first', sparse_output = False, handle_unknown='ignore')
train_inputs.head(2)

train_cat = encoder.fit_transform(train_inputs[cat_cols])
test_cat = encoder.transform(test_input[cat_cols])

# updating numerical columns
num_cols = num_cols.drop(['Aggregate rating'])

scaler = StandardScaler()
train_num = scaler.fit_transform(train_inputs[num_cols])
test_num = scaler.transform(test_input[num_cols])

train_num

test_num

# Combining
train_processed = np.hstack((train_num, train_cat))
test_processed = np.hstack((test_num, test_cat))

train_processed

"""## Model Selection"""

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

"""### **Using Linear Regression**"""

model = LinearRegression()

model.fit(train_processed, train_targets)

train_pred = model.predict(train_processed)
test_pred = model.predict(test_processed)

"""## Model Evaluation"""

train_mse = mean_squared_error(train_targets, train_pred)
train_mae = mean_absolute_error(train_targets, train_pred)

train_mse, train_mae

test_mse = mean_squared_error(test_target, test_pred)
test_mae = mean_absolute_error(test_target, test_pred)

test_mse, test_mae

"""## Model Performance"""

train_score = r2_score(train_targets, train_pred)
test_score = r2_score(test_target, test_pred)

train_score, test_score

"""### **Using Decision tree regressor**"""

model = DecisionTreeRegressor()

model.fit(train_processed, train_targets)

train_pred = model.predict(train_processed)
test_pred = model.predict(test_processed)

train_pred

"""## Model Evaluation"""

train_mse = mean_squared_error(train_targets, train_pred)
train_mae = mean_absolute_error(train_targets, train_pred)

train_mse, train_mae

test_mse = mean_squared_error(test_target, test_pred)
test_mae = mean_absolute_error(test_target, test_pred)

test_mse, test_mae

"""## Model Performance"""

train_score = r2_score(train_targets, train_pred)
test_score = r2_score(test_target, test_pred)

train_score, test_score

"""### **Using Random forest**"""

model = RandomForestRegressor()

model.fit(train_processed, train_targets)

train_pred = model.predict(train_processed)
test_pred = model.predict(test_processed)

"""## Model Evaluation"""

train_mse = mean_squared_error(train_targets, train_pred)
train_mae = mean_absolute_error(train_targets, train_pred)

train_mse, train_mae

test_mse = mean_squared_error(test_target, test_pred)
test_mae = mean_absolute_error(test_target, test_pred)

test_mse, test_mae

"""## Model Performance"""

train_score = r2_score(train_targets, train_pred)
test_score = r2_score(test_target, test_pred)

train_score, test_score

# Comparing algorithms
algorithm_names = ['Linear Regression', 'Decision Tree', 'Random Forest']
r2_scores = [-2652530.1468, 0.9778, 0.9874]

df_scores = pd.DataFrame({'Algorithm': algorithm_names, 'R2 Score': r2_scores})

df_scores

"""The best model I used is the random forest model.

I went through the whole analysis and machine learning process without transforming my columns, some of them contained outliers but I went about it like that. Going through this project work draws insight towards a lot of things.
"""

from google.colab import drive
drive.mount('/content/drive')