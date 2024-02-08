# -*- coding: utf-8 -*-
"""avishkar_task1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1srUn74B9li9WoKLkLwniRrejHCoki3-r
"""

# Import necessary libraries
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Load Titanic dataset
titanic = sns.load_dataset('titanic')

# Data preprocessing
# Drop unnecessary columns
titanic = titanic.drop(['deck', 'embark_town', 'alive'], axis=1)

# Impute missing values
imputer = SimpleImputer(strategy='most_frequent')
titanic['embarked'] = imputer.fit_transform(titanic[['embarked']])
titanic['embarked'] = LabelEncoder().fit_transform(titanic['embarked'])

# Convert categorical variables into numerical using one-hot encoding
titanic = pd.get_dummies(titanic, columns=['sex', 'class', 'who', 'adult_male'])

# Feature engineering
titanic['family_size'] = titanic['sibsp'] + titanic['parch'] + 1

# Select features and target variable
X = titanic.drop('survived', axis=1)
y = titanic['survived']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build a pipeline for preprocessing and model training
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(random_state=42))
])

# Define hyperparameters for tuning
param_grid = {
    'imputer__strategy': ['mean', 'median'],
    'classifier__n_estimators': [50, 100, 150],
    'classifier__max_depth': [None, 10, 20],
    'classifier__min_samples_split': [2, 5, 10],
    'classifier__min_samples_leaf': [1, 2, 4]
}

# Perform GridSearchCV for hyperparameter tuning
grid_search = GridSearchCV(pipeline, param_grid=param_grid, cv=5, scoring='accuracy', verbose=1)
grid_search.fit(X_train, y_train)

# Get the best parameters
best_params = grid_search.best_params_
print("Best Hyperparameters:", best_params)

# Make predictions on the test set
y_pred = grid_search.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy:.2f}")
print("Confusion Matrix:\n", conf_matrix)
print("Classification Report:\n", classification_rep)