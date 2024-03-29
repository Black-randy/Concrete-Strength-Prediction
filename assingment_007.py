# -*- coding: utf-8 -*-
"""Assingment_007

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13vx743T-fZaw794zBwXUTIoT6wc0yv07
"""

# @title **Step 0 :** Get Necessary Libraries
!pip install seaborn
!pip install wget pandas

import numpy as np
import pandas as pd

import tensorflow as tf

import wget
import os
import shutil




from IPython.display import display
from IPython.display import clear_output
from IPython.display import clear_output

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.cluster import KMeans

import seaborn as sns
import matplotlib.pyplot as plt

# @title **Step 1 :** Download From Github and Organize Data

# Install wget and pandas (if not already installed)


# Function to download and organize data
def download_and_organize_data():

    # URLs of the files on GitHub

    # url_concrete = "https://raw.githubusercontent.com/Black-randy/Concrete-Strength-Prediction/main/concrete.csv"
    url_concrete_data_yeh = "https://raw.githubusercontent.com/Black-randy/Concrete-Strength-Prediction/main/Concrete_Data_Yeh.csv"

    # Specify the destination paths in Google Colab
    destination_path_train = "/content/train_data/Concrete_Data_Yeh.csv"
    # destination_path_test = "/content/test_data/concrete.csv"

    # Create folders for test and train data
    os.makedirs("/content/train_data", exist_ok=True)
    # os.makedirs("/content/test_data", exist_ok=True)

    # Download the files
    wget.download(url_concrete_data_yeh, destination_path_train)
    # wget.download(url_concrete, destination_path_test)
    clear_output()
    # Print a message indicating the completion of the download and organization
    print("Files downloaded and organized into train_data and test_data folders.")

# Download and organize data
download_and_organize_data()

# @title **Step 2 :** Load Data into Pandas DataFrames
# Function to load data into Pandas DataFrames
def load_data_into_dataframes():
    # Assign values to train_data_path and test_data_path
    train_data_path = "/content/train_data"
    # test_data_path = "/content/test_data"

    # Load CSV files into Pandas DataFrames
    train_df = pd.read_csv(os.path.join(train_data_path, "Concrete_Data_Yeh.csv"))
    # test_df = pd.read_csv(os.path.join(test_data_path, "concrete.csv"))

    # Clear previous outputs
    clear_output()

    # Print the assigned values and display a preview of the DataFrames
    print(f"train_data_path: {train_data_path}")
    # print(f"test_data_path: {test_data_path}")

    # Return the DataFrames
    return train_df # ,test_df

# Load data into Pandas DataFrames
train_df = load_data_into_dataframes()

# @title **Step 2.1 :** Train DataFrame info

print("\nShape of the data :-\n")
rows_count, columns_count = train_df.shape
print('Total Number of rows :', rows_count)
print('Total Number of columns :', columns_count)

# Display a preview of the train DataFrame
print("\n\nPreview of train DataFrame:\n")
display(train_df.head(10))


# Display data types of each attribute in the train DataFrame
train_data_types = train_df.dtypes
print("\n\nData Types of Attributes in Train DataFrame:\n")
print(train_data_types)

# Check for missing values in the train DataFrame
missing_values_train = train_df.isnull().sum()

# Check for missing values in the test DataFrame
# missing_values_test = test_df.isnull().sum()

# Display the results
print("\n\nMissing Values in Train DataFrame:\n")
print(missing_values_train[missing_values_train > 0])

# print("\nMissing Values in Test DataFrame:")
# print(missing_values_test[missing_values_test > 0])

# Display descriptive statistics for the train DataFrame
train_descriptive_stats = train_df.describe()

# Display descriptive statistics for the test DataFrame
# test_descriptive_stats = test_df.describe()

# Print the results
print("\n\nDescriptive Statistics for Train DataFrame:")
print(train_descriptive_stats)

# print("\nDescriptive Statistics for Test DataFrame:")
# print(test_descriptive_stats)

# @title **Step 3 :** Visualize Feature Importances

# Concatenate train and test data for modeling
combined_df = pd.concat([train_df], ignore_index=True)
# combined_df = pd.concat([train_df, test_df], ignore_index=True)

# Separate features and target variable
X = combined_df.drop(columns=['csMPa'])
y = combined_df['csMPa']

# Create a Random Forest Regressor
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

# Fit the model
rf_model.fit(X, y)

# Get feature importances
feature_importances = rf_model.feature_importances_

# Create a DataFrame to hold feature names and their importances
feature_importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': feature_importances})

# Sort features by importance in descending order
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

# Plot the feature importances
plt.figure(figsize=(10, 6))
plt.barh(feature_importance_df['Feature'], feature_importance_df['Importance'])
plt.xlabel('Importance')
plt.title('Feature Importances')
plt.show()

# @title Pair Plot of All Columns

#Set the style of seaborn
# sns.set(style="ticks")

#Create a pair plot for all columns
# plt.figure(figsize=(18, 15))
# sns.pairplot(combined_df, markers="h", diag_kind='kde')
# plt.suptitle("Pair Plot of All Columns", y=1.02, fontsize=20)
# plt.show()

# @title Visualize Outliers

# Set the style of seaborn
sns.set(style="whitegrid")

# Select relevant columns for visualization
columns_of_interest = ['cement', 'slag', 'flyash', 'water', 'superplasticizer', 'coarseaggregate', 'fineaggregate', 'age', 'csMPa']

# Create a horizontal box plot for each column to visualize outliers
plt.figure(figsize=(12, 6))
sns.boxplot(data=combined_df[columns_of_interest], orient="h", palette="Set2", dodge=False)
plt.title('Horizontal Box Plot of Features to Visualize Outliers')
plt.show()

"""# **Outliers Visualization**
---
"""

'''
# @title Outliers Visualization
features_of_interest = ['cement', 'slag', 'flyash', 'water', 'superplasticizer', 'coarseaggregate', 'fineaggregate', 'age', 'csMPa']

# Set the style of seaborn
sns.set(style="whitegrid")

# Create subplots
fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(6,6))

# Flatten the axes for easy iteration
axes = axes.flatten()

# Loop through each feature and create histograms and boxplots
for i, feature in enumerate(features_of_interest):
    sns.histplot(train_df[feature], kde=True, ax=axes[i])
    axes[i].set_xlabel(feature, fontsize=8)
    axes[i].set_title(f"{feature} Distribution Plot", fontsize=8)

# Adjust layout
plt.tight_layout()
plt.show()

# Box plots for each feature
fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(6,6))

# Flatten the axes for easy iteration
axes = axes.flatten()

# Loop through each feature and create boxplots
for i, feature in enumerate(features_of_interest):
    sns.boxplot(train_df[feature], ax=axes[i])
    axes[i].set_xlabel(feature, fontsize=8)
    axes[i].set_title(f"{feature} Box Plot", fontsize=8)

# Adjust layout
plt.tight_layout()
plt.show()
'''

# @title Cement Outliers Visualization
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(13, 5))
fig.set_size_inches(10,3)

sns.histplot(train_df['cement'], ax=ax1, kde=True)
ax1.tick_params(labelsize=15)
ax1.set_xlabel('Cement', fontsize=15)
ax1.set_title("Distribution Plot")

sns.boxplot(train_df['cement'], ax=ax2)
ax2.set_title("Box Plot")
ax2.set_xlabel('Cement', fontsize=15)

# @title Slag Outliers Visualization
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(13, 5))
fig.set_size_inches(10,3)
sns.histplot(train_df['slag'], ax=ax1, kde=True)
ax1.set_xlabel('Slag', fontsize=15)
ax1.set_title("Distribution Plot")

sns.boxplot(train_df['slag'], ax=ax2)
ax2.set_xlabel('Slag', fontsize=15)
ax2.set_title("Box Plot")

# @title  Flyash Outliers Visualization
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(13, 5))
fig.set_size_inches(10,3)
sns.histplot(train_df['flyash'], ax=ax1, kde=True)
ax1.set_xlabel('Flyash', fontsize=15)
ax1.set_title("Distribution Plot")

sns.boxplot(train_df['flyash'], ax=ax2)
ax2.set_xlabel('Flyash', fontsize=15)
ax2.set_title("Box Plot")

# @title  Water Outliers Visualization
# Water
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(13, 5))
fig.set_size_inches(10,3)
sns.histplot(train_df['water'], ax=ax1, kde=True)
ax1.set_xlabel('Water', fontsize=15)
ax1.set_title("Distribution Plot")

sns.boxplot(train_df['water'], ax=ax2)
ax2.set_xlabel('Water', fontsize=15)
ax2.set_title("Box Plot")

# @title  Superplasticizer Outliers Visualization
# Superplasticizer
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(13, 5))
fig.set_size_inches(10,3)

sns.histplot(train_df['superplasticizer'], ax=ax1, kde=True)
ax1.set_xlabel('Superplasticizer', fontsize=15)
ax1.set_title("Distribution Plot")

sns.boxplot(train_df['superplasticizer'], ax=ax2)
ax2.set_xlabel('Superplasticizer', fontsize=15)
ax2.set_title("Box Plot")

# @title  Coarseagg Outliers Visualization
# Coarseagg
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(13, 5))
fig.set_size_inches(10,3)
sns.histplot(train_df['coarseaggregate'], ax=ax1, kde=True)
ax1.set_xlabel('Coarseagg', fontsize=15)
ax1.set_title("Distribution Plot")

sns.boxplot(train_df['coarseaggregate'], ax=ax2)
ax2.set_xlabel('Coarseagg', fontsize=15)
ax2.set_title("Box Plot")

# @title  Fineaggregate Outliers Visualization
# Fineaggregate
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(13, 5))
fig.set_size_inches(10,3)
sns.histplot(train_df['fineaggregate'], ax=ax1, kde=True)
ax1.set_xlabel('Fineagg', fontsize=15)
ax1.set_title("Distribution Plot")

sns.boxplot(train_df['fineaggregate'], ax=ax2)
ax2.set_xlabel('Fineagg', fontsize=15)
ax2.set_title("Box Plot")

# @title  Age Outliers Visualization
# Age
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(13, 5))
fig.set_size_inches(10,3)
sns.histplot(train_df['age'], ax=ax1, kde=True)
ax1.set_xlabel('Age', fontsize=15)
ax1.set_title("Distribution Plot")

sns.boxplot(train_df['age'], ax=ax2)
ax2.set_xlabel('Age', fontsize=15)
ax2.set_title("Box Plot")

Q1_age = train_df['age'].quantile(0.25)
Q3_age = train_df['age'].quantile(0.75)
IQR_age = Q3_age - Q1_age
LTV_age = Q1_age - 1.5 * IQR_age
UTV_age = Q3_age + 1.5 * IQR_age

# @title  Strength Outliers Visualization

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(13, 5))
fig.set_size_inches(10,3)
sns.histplot(train_df['csMPa'], ax=ax1, kde=True)
ax1.tick_params(labelsize=15)
ax1.set_xlabel('Strength', fontsize=15)
ax1.set_title("Distribution Plot")

sns.boxplot(train_df['csMPa'], ax=ax2)
ax2.set_title("Box Plot")
ax2.set_xlabel('Strength', fontsize=15)

"""# **Fixing Outliers**
---
"""

# Create a new DataFrame for fixing outliers
train_df_new = train_df.copy()

# Iterate over each column (excluding the last one, assuming it's the target variable)
for col_name in train_df_new.columns[:-1]:
    q1 = train_df_new[col_name].quantile(0.25)
    q3 = train_df_new[col_name].quantile(0.75)
    iqr = q3 - q1
    low = q1 - 1.5 * iqr
    high = q3 + 1.5 * iqr

    # Replace values outside the lower and upper bounds with the median of the column
    train_df_new.loc[(train_df_new[col_name] < low) | (train_df_new[col_name] > high), col_name] = train_df_new[col_name].median()

# Set the style of seaborn
sns.set(style="whitegrid")

# Plot boxplot after fixing outliers
plt.figure(figsize=(15, 8))
sns.boxplot(data=train_df_new, orient="h", palette="Set2", dodge=False)
plt.title('Box Plot after Fixing Outliers')
plt.show()

# @title  Calculate the correlation matrix
# train_df_new.corr() //// ----------- for insight

correlation_matrix = train_df_new.corr()

# Create a mask for the upper triangle
mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))

# Set up the matplotlib figure with seaborn style
with sns.axes_style("white"):
    plt.figure(figsize=(12, 10))

    # Draw the heatmap with the mask
    sns.heatmap(correlation_matrix,cmap="RdPu", annot=True, fmt=".2f", linewidths=".5")

    # Set the title
    plt.title("Correlation Matrix for Train DataFrame", fontsize=16)

# The plot will be shown automatically when the code block is executed

# @title  KMeans clustering algorithm to find the optimal number of clusters

cluster_range = range(2, 6)
cluster_errors = []

for num_clusters in cluster_range:
    clusters_df = KMeans(num_clusters, n_init=5)
    clusters_df.fit(train_df_new)
    labels = clusters_df.labels_
    centroids = clusters_df.cluster_centers_
    cluster_errors.append(clusters_df.inertia_)

clusters_df = pd.DataFrame({"num_clusters": cluster_range, "cluster_errors": cluster_errors})
print(clusters_df)
# Elbow plot
plt.figure(figsize=(4, 3))
plt.plot(clusters_df.num_clusters, clusters_df.cluster_errors, marker="o")
plt.title('Elbow Plot for Optimal Number of Clusters')
plt.xlabel('Number of Clusters')
plt.ylabel('Cluster Errors (Inertia)')
print('\n')
plt.show()

# @title  Assigne cluster IDs to each data point
num_clusters = 3 # @param {type:"integer"}

# Create a KMeans model with the specified number of clusters
kmeans_model = KMeans(n_clusters=num_clusters, random_state=2354)

# Fit the model to the training data
kmeans_model.fit(train_df_new)

# Predict the cluster labels for each data point
cluster_labels = kmeans_model.predict(train_df_new)

# Assign the cluster labels to the original DataFrame
train_df_new["Cluster_id"] = cluster_labels

# Create a deep copy of the DataFrame with cluster assignments
train_df_new_clustered = train_df_new.copy(deep=True)

# already fitted a KMeans model named 'kmeans_model'
centroids = kmeans_model.cluster_centers_

# 'centroids' is now a NumPy array containing the coordinates of the cluster centers
print("Cluster Centers:")
centroids

# centroids_df = pd.DataFrame(centroids, columns=train_df_new.columns[:-1])  # Exclude the 'Cluster_id' column
# print("Cluster Centers (DataFrame):")
# print(centroids_df)

from scipy.stats import zscore

train_df_Scaled = train_df_new.apply(zscore)
# display(train_df_Scaled.head(5))
# print('\n')
# plt.figure(figsize=(6,3))
# sns.boxplot(data=train_df_Scaled, orient="h", palette="Set2", dodge=False)

"""# **Negelect theese**"""

train_df.head()

train_df_new.head()

train_df_Scaled.head()

"""# **DATA** Test Splitting"""

# @title **Step xx :** Separating  **csMPa**  --- not in use
# x = train_df_new.drop(columns=['csMPa'])
# y = train_df_new['csMPa']

from sklearn.model_selection import train_test_split

# @title **Step xx :** Separating  **csMPa** (Scaled)
y = train_df_Scaled['csMPa']
x = train_df_Scaled.drop(columns=['csMPa'])

# Perform train-test split
x_model_train, x_test, y_model_train, y_test = train_test_split(x, y, test_size=0.2, random_state=7)

# Display the shapes of the resulting data sets
print('x_train data shape :{}'.format(x_model_train.shape))
print('y_train data shape :{}'.format(y_model_train.shape))
print('x_test data shape  :{}'.format(x_test.shape))
print('y_test data shape  :{}'.format(y_test.shape))

# @title **Step xx :** Separating  **csMPa** (Scaled)
# Perform train-test split
x_train, x_validate, y_train, y_validate = train_test_split(x_model_train, y_model_train, test_size=0.3, random_state=7)

# Display the shapes of the resulting data sets
print('x_train data shape :{}'.format(x_train.shape))
print('y_train data shape :{}'.format(y_train.shape))
print('x_test data shape  :{}'.format(x_validate.shape))
print('y_test data shape  :{}'.format(y_validate.shape))

"""# **Models**"""

# @title Defining the kFold function for the cross validation
from sklearn.model_selection import KFold
import numpy as np
# Define the number of splits and random state
n_splits = 10
random_state = 7

# Set the random seed using numpy
np.random.seed(random_state)

# Create a KFold object with shuffle=False
kfold = KFold(n_splits=n_splits, shuffle=False)

linear_model = []
linear_model_score = []
linear_model_RMSE = []
linear_model_R_2 = []
Model = []
RMSE = []
R_sq = []

# @title **Model X.1 :** Linear Regression Model
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, KFold

# Initialize Linear Regression model
regression_model = LinearRegression()

# Fit the Linear Regression model on the training data
regression_model.fit(x_train, y_train)

# Append the model name to the list
linear_model.append('Linear Regression')

# Add a space
print("\n" + "-"*13 + "Linear Regression Model" + "-"*13 + "\n")

# Display coefficients for each independent attribute
for idx, col_name in enumerate(x_train.columns):
    print("The coefficient for {} is:{} ".format(col_name, regression_model.coef_[idx]))

print("\n" + "-"*50 + "\n")

# Display the intercept for the model
intercept = regression_model.intercept_
print("Model intercept is {}".format(intercept))

# Evaluate the model on the validation set
lr_score = regression_model.score(x_validate, y_validate)
linear_model_score.append(lr_score)
print("Linear Regression Model Score:", lr_score)

# Calculate RMSE using cross-validation
kfold = KFold(n_splits=10, shuffle=True, random_state=7)
lr_rmse = np.sqrt((-1) * cross_val_score(regression_model, x_train, y_train.values.ravel(), cv=kfold, scoring='neg_mean_squared_error').mean())
print("Linear Regression Model RMSE :", lr_rmse)

# Append RMSE to the list
linear_model_RMSE.append(lr_rmse)

# Calculate R-squared using cross-validation
lr_r2 = cross_val_score(regression_model, x_train, y_train.values.ravel(), cv=kfold, scoring='r2').mean()
print("Linear Regression Model R-Square Value :", lr_r2)

# Append R-squared to the list
linear_model_R_2.append(lr_r2)
# Add a space
print("\n" + "-"*50 + "\n")

# Scatter plot with labels and title
#   plt.figure(figsize=(5, 5))
#   plt.scatter(y_test, y_predict, alpha=0.5)
#   plt.title("Actual vs Predicted Concrete Strength")
#   plt.xlabel("Actual Concrete Strength")
#   plt.ylabel("Predicted Concrete Strength")
#   plt.show()

# @title **Model X.2 :** Multilinear Regression Model

# Import necessary libraries for Multilinear Regression
from sklearn.linear_model import LinearRegression

# Initialize Multilinear Regression model
mlr_model = LinearRegression()

# Fit the Multilinear Regression model on the training data
mlr_model.fit(x_train, y_train)

# Append the model name to the list
linear_model.append('Multilinear Regression')

# Add a space
print("\n" + "-"*13 + "Multilinear Regression Model" + "-"*13 + "\n")

# Display coefficients for each independent attribute
print("Coefficients for each independent attribute:")
for idx, col_name in enumerate(x_train.columns):
    print("The coefficient for {} is: {}".format(col_name, mlr_model.coef_[idx]))

print("\n" + "-"*50 + "\n")

# Evaluate the model on the validation set
mlr_score = mlr_model.score(x_validate, y_validate)
linear_model_score.append(mlr_score)
print("Multilinear Regression Model Score:", mlr_score)

# Calculate RMSE using cross-validation
mlr_rmse = np.sqrt((-1) * cross_val_score(mlr_model, x_train, y_train.values.ravel(), cv=kfold, scoring='neg_mean_squared_error').mean())
print("Multilinear Regression Model RMSE :", mlr_rmse)

# Append RMSE to the list
linear_model_RMSE.append(mlr_rmse)

# Calculate R-squared using cross-validation
mlr_r2 = cross_val_score(mlr_model, x_train, y_train.values.ravel(), cv=kfold, scoring='r2').mean()
print("Multilinear Regression Model R-Square Value :", mlr_r2)

# Append R-squared to the list
linear_model_R_2.append(mlr_r2)
# Add a space
print("\n" + "-"*50 + "\n")

# @title <del> **Model xx :**  Train Random Forest Classifier. </del>

'''
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Convert the target variable to binary labels for classification
threshold = 1
y_train_class = (y_train > threshold).astype(int)
y_test_class = (y_test > threshold).astype(int)

# Create and fit the Random Forest Classifier model
rf_classifier_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier_model.fit(x_train, y_train_class)

# Make predictions on the test data
y_predict_class = rf_classifier_model.predict(x_test)

# Evaluate the Random Forest Classifier performance
accuracy = accuracy_score(y_test_class, y_predict_class)
classification_rep = classification_report(y_test_class, y_predict_class)
conf_matrix = confusion_matrix(y_test_class, y_predict_class)

# Print performance metrics
print("Accuracy:", accuracy)
print("\nClassification Report:\n", classification_rep)
print("\nConfusion Matrix:\n", conf_matrix)

# Plot the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='g', cmap='Blues', xticklabels=['Not High Strength', 'High Strength'],
            yticklabels=['Not High Strength', 'High Strength'])
plt.title('Confusion Matrix for Random Forest Classifier')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()'''

"""-adding Random  and modifying -"""

# @title **Model X.3 :** Random Forest Regressor Model
from sklearn.ensemble import RandomForestRegressor
n_estimators = [int(x) for x in np.linspace(start = 10 , stop = 100, num = 3)]
# Create a Random Forest Regressor
rfTree = RandomForestRegressor()

# Fit the Random Forest Regressor on the training data
rfTree.fit(x_train, y_train.values.ravel())


# Add a space
print("\n" + "-"*13 + "Random Forest Regressor Model" + "-"*13 + "\n")

# Evaluate the model on the training set
rfTree_train_score = rfTree.score(x_train, y_train)
print("Random Forest Regressor Model Training Set Score:", rfTree_train_score)

# Evaluate the model on the validation set
rfTree_score = rfTree.score(x_validate, y_validate)
linear_model_score.append(rfTree_score)
print("Random Forest Regressor Model Validation Set Score:", rfTree_score)

# Calculate RMSE using cross-validation
rfTree_rmse = np.sqrt((-1) * cross_val_score(rfTree, x_train, y_train.values.ravel(), cv=kfold, scoring='neg_mean_squared_error').mean())
print("Random Forest Regressor Model RMSE:", rfTree_rmse)

# Calculate R-squared using cross-validation
rfTree_r2 = cross_val_score(rfTree, x_train, y_train.values.ravel(), cv=kfold, scoring='r2').mean()
print("Random Forest Regressor Model R-Square Value:", rfTree_r2)

# Add a space
print("\n" + "-"*50 + "\n")

# Create a DataFrame with model metrics
rfTree_model_df = pd.DataFrame({'Trainng Score': [rfTree_train_score],
                                'Validation Score': [rfTree_score],
                                'RMSE': [rfTree_rmse],
                                'R Squared': [rfTree_r2]})
display(rfTree_model_df)
print("\n" + "-"*50 + "\n")
rfTree_test_score = rfTree.score(x_test, y_test)
print("Random Forest Regressor Model Test Data Set Score:", rfTree_test_score)

# @title **Model X.3.1 :** Hyper-tuning Random Forest Regressor -  **Gridsearch CV**
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint as sp_randint
import sys

# Define the parameter distribution
param_dist = {
    'bootstrap': [True],
    'max_depth': [10],
    'max_features': ['log2'],
    'min_samples_leaf': [1, 2, 3],
    'min_samples_split': sp_randint(5, 11),
    'n_estimators': sp_randint(50, 71)
}

# Create a Random Forest Regressor
rf_model = RandomForestRegressor(random_state=7)

# Create RandomizedSearchCV
random_search = RandomizedSearchCV(estimator=rf_model, param_distributions=param_dist, n_iter=10, cv=kfold, n_jobs=1, verbose=0, return_train_score=True, random_state=7)

# Redirect standard output to capture progress
original_stdout = sys.stdout
sys.stdout = sys.stderr

# Fit the random search to the data
print("Fitting RandomizedSearchCV...")
random_search.fit(x_train, y_train.values.ravel())

# Reset standard output
sys.stdout = original_stdout

# Get the best parameters and model
best_params = random_search.best_params_
best_rf_model = random_search.best_estimator_

# Print the best parameters
print("Best Parameters:")
for param, value in best_params.items():
    print(f"{param}: {value}")


# Add a space
print("\n" + "-"*50 + "\n")

# Fit the best model on the training set
best_rf_model.fit(x_train, y_train.values.ravel())

# Evaluate the best model on the validation set
best_rf_score_val = best_rf_model.score(x_validate, y_validate)
print("Best Random Forest Regressor Model Validation Set Score:", best_rf_score_val)

# Calculate RMSE using cross-validation
best_rf_rmse = np.sqrt((-1) * cross_val_score(best_rf_model, x_train, y_train.values.ravel(), cv=kfold, scoring='neg_mean_squared_error').mean())
print("Best Random Forest Regressor Model RMSE:", best_rf_rmse)

# Calculate R-squared using cross-validation
best_rf_r2 = cross_val_score(best_rf_model, x_train, y_train.values.ravel(), cv=kfold, scoring='r2').mean()
print("Best Random Forest Regressor Model R-Square Value:", best_rf_r2)

# Create a DataFrame with model metrics
best_rf_model_df = pd.DataFrame({'Training Score': [best_rf_model.score(x_train, y_train)],
                                'Validation Score': [best_rf_score_val],
                                'RMSE': [best_rf_rmse],
                                'R Squared': [best_rf_r2]})
display(best_rf_model_df)