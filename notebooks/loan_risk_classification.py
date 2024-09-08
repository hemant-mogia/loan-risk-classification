# -*- coding: utf-8 -*-
"""loan_risk_classification-v2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1d6Lk4hL2so0U-xr6WQCphpCJxMmCNV3R
"""

from google.colab import drive
drive.mount('/content/drive')

def load_data(train_path, test_path):
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)
    return train, test

import pandas as pd

# Load data
test, train  = load_data('/content/drive/MyDrive/bureau/Assignment_Test.csv', '/content/drive/MyDrive/bureau/Assignment_Train.csv')

train.head()

# List of columns to consider as features for training the model
train_cols_to_consider = [
    # Application Details
    # 'APPLICATION LOGIN DATE',
    'AADHAR VERIFIED',

    # Financial Information
    'Cibil Score',
    'TOTAL ASSET COST',
    'APPLIED AMOUNT',

    # Demographics
    'MARITAL STATUS',
    'GENDER',
    'DOB',
    'AGE',

    # Phone Related Features
    'phone_digitalage',
    'phone_nameMatchScore',
    'phone_phoneFootprintStrengthOverall'

    # Target Variable
    'Application Status'
]

print(train.columns.tolist())

# List of columns to consider as features for training the model
train_cols_to_consider = [
    # Application Details
    # 'APPLICATION LOGIN DATE',
    'AADHAR VERIFIED',

    # Financial Information
    'Cibil Score',
    'TOTAL ASSET COST',
    'APPLIED AMOUNT',

    # Demographics
    'MARITAL STATUS',
    'GENDER',
    'AGE',

    # Phone Related Features
    'phone_digitalage',
    'phone_nameMatchScore',
    'phone_phoneFootprintStrengthOverall',

    # Target Variable
    'Application Status'
]

# Check the existing columns
existing_columns = train.columns.tolist()
missing_columns = [col for col in train_cols_to_consider if col not in existing_columns]

if missing_columns:
    print(f"Columns missing from DataFrame: {missing_columns}")
else:
    # If all columns exist, create the DataFrame with selected columns
    train_df = train[train_cols_to_consider]
    print("Columns selected successfully.")

train_df.head()

pd.set_option('display.max_columns', None)
train_df.head(10)

target = train_df['Application Status']

train_df = train_df.drop('Application Status', axis=1)

target.value_counts()

target = target.map({'APPROVED': 1, 'DECLINED': 0})

target.value_counts()

print(train_df.isnull().sum()[train_df.isnull().sum() > 0])

print(train_df[['Cibil Score', 'TOTAL ASSET COST']].dtypes)

import pandas as pd
from sklearn.impute import KNNImputer

# Impute 'Single' for missing MARITAL_STATUS
train_df.loc[:, 'MARITAL STATUS'] = train_df['MARITAL STATUS'].fillna('Single')

# Convert columns to numeric
train_df.loc[:, 'Cibil Score'] = pd.to_numeric(train_df['Cibil Score'], errors='coerce')
train_df.loc[:, 'TOTAL ASSET COST'] = pd.to_numeric(train_df['TOTAL ASSET COST'], errors='coerce')

# Create a new DataFrame for the columns to be imputed
impute_df = train_df[['Cibil Score', 'TOTAL ASSET COST']].copy()

# KNN imputer for Cibil Score and TOTAL ASSET COST
imputer = KNNImputer(n_neighbors=5)
imputed_values = imputer.fit_transform(impute_df)

# Assign the imputed values back to the original DataFrame
train_df.loc[:, ['Cibil Score', 'TOTAL ASSET COST']] = imputed_values

print(train_df.isnull().sum()[train_df.isnull().sum() > 0])

# Convert columns to numeric
train_df.loc[:, 'phone_digitalage'] = pd.to_numeric(train_df['phone_digitalage'], errors='coerce')
train_df.loc[:, 'phone_nameMatchScore'] = pd.to_numeric(train_df['phone_nameMatchScore'], errors='coerce')

# Interpolation for missing values
train_df.loc[:, 'phone_digitalage'] = train_df['phone_digitalage'].interpolate()
train_df.loc[:, 'phone_nameMatchScore'] = train_df['phone_nameMatchScore'].interpolate()
train_df['phone_phoneFootprintStrengthOverall'] = train_df['phone_phoneFootprintStrengthOverall'].astype('object')
train_df['phone_phoneFootprintStrengthOverall'] = train_df['phone_phoneFootprintStrengthOverall'].fillna('Low')

train_df['Cibil Score'] = train_df['Cibil Score'].astype('float64')

train_df.head()

print(train_df.isnull().sum())

train_df.info()

# Select columns with object data type
pd.set_option('display.max_columns', None)
object_columns = train_df.select_dtypes(include='object')

object_columns

object_columns.info()

# Use value_counts() on each column
for col in object_columns.columns:
  print(f"\nUnique Value Counts for Column '{col}':")
  print(object_columns[col].value_counts())

# Select columns with object data type
pd.set_option('display.max_columns', None)
num_columns = train_df.select_dtypes(include='float64')

num_columns.info()



from sklearn.preprocessing import LabelEncoder, StandardScaler

# Initialize LabelEncoder
le = LabelEncoder()

# Label encode object columns
encoded_object_df = object_columns.copy()
for col in object_columns.columns:
    encoded_object_df[col] = le.fit_transform(object_columns[col])

# Initialize StandardScaler
scaler = StandardScaler()

# Scale numerical columns
scaled_numerical_df = pd.DataFrame(scaler.fit_transform(num_columns), columns=num_columns.columns)

# Combine encoded object columns with scaled numerical columns
final_df = pd.concat([encoded_object_df, scaled_numerical_df], axis=1)

# Display the updated DataFrame
print(final_df.head())

final_df.head()

final_df.shape, target.shape

# for data processing and manipulation
import pandas as pd
import numpy as np

# scikit-learn modules for feature selection and model evaluation
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFE, SelectKBest, SelectFromModel, chi2, f_classif
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, precision_score, recall_score, f1_score
from sklearn.svm import LinearSVC
from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# libraries for visualization
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

X, Y = final_df, target



def fit_model(X, Y):
    '''Use a RandomForestClassifier for this problem.'''

    # define the model to use
    model = RandomForestClassifier(criterion='entropy', random_state=47)

    # Train the model
    model.fit(X, Y)

    return model

def calculate_metrics(model, X_test_scaled, Y_test):
    '''Get model evaluation metrics on the test set.'''

    # Get model predictions
    y_predict_r = model.predict(X_test_scaled)

    # Calculate evaluation metrics for assesing performance of the model.
    acc = accuracy_score(Y_test, y_predict_r)
    roc = roc_auc_score(Y_test, y_predict_r)
    prec = precision_score(Y_test, y_predict_r)
    rec = recall_score(Y_test, y_predict_r)
    f1 = f1_score(Y_test, y_predict_r)

    return acc, roc, prec, rec, f1

def train_and_get_metrics(X, Y):
    '''Train a Random Forest Classifier and get evaluation metrics'''

    # Split train and test sets
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2,stratify=Y, random_state = 123)

    # All features of dataset are float values. You normalize all features of the train and test dataset here.
    scaler = StandardScaler().fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Call the fit model function to train the model on the normalized features and the diagnosis values
    model = fit_model(X_train_scaled, Y_train)

    # Make predictions on test dataset and calculate metrics.
    acc, roc, prec, rec, f1 = calculate_metrics(model, X_test_scaled, Y_test)

    return acc, roc, prec, rec, f1

def evaluate_model_on_features(X, Y):
    '''Train model and display evaluation metrics.'''

    # Train the model, predict values and get metrics
    acc, roc, prec, rec, f1 = train_and_get_metrics(X, Y)

    # Construct a dataframe to display metrics.
    display_df = pd.DataFrame([[acc, roc, prec, rec, f1, X.shape[1]]], columns=["Accuracy", "ROC", "Precision", "Recall", "F1 Score", 'Feature Count'])

    return display_df

# Calculate evaluation metrics
all_features_eval_df = evaluate_model_on_features(X, Y)
all_features_eval_df.index = ['All features']

# Initialize results dataframe
results = all_features_eval_df

# Check the metrics
results.head()

import seaborn as sns
import matplotlib.pyplot as plt

# Set the figure size
plt.figure(figsize=(10, 8))  # Adjust size for better visibility

# Calculate the correlation matrix
cor = X.corr()

# Create the heatmap with minimalistic design
sns.heatmap(
    cor,
    annot=True,  # Show correlation values on the heatmap
    cmap='coolwarm',  # Simple color map for the heatmap
    fmt='.2f',  # Format for the annotation text
    linewidths=0.3,  # Minimal width of the lines separating the cells
    linecolor='lightgrey',  # Light color for the lines separating the cells
    cbar_kws={
        'shrink': .8,  # Shrink color bar for better fit
        'label': 'Correlation'  # Label for the color bar
    },
    annot_kws={"size": 8, "color": "black"}  # Smaller, minimal annotation text
)

# Add plot title and axis labels
plt.title('Feature Correlation Matrix', size=16, weight='bold')  # Title of the heatmap
plt.xlabel('Features', size=12)  # X-axis label
plt.ylabel('Features', size=12)  # Y-axis label

# Remove unnecessary grid lines
plt.grid(False)

# Display the plot
plt.tight_layout()  # Adjust layout to prevent clipping of labels
plt.show()

# Get the absolute value of the correlation
cor_target = abs(X.corrwith(Y))

# Select highly correlated features (threshold = 0.02)
highly_correlated_features = cor_target[cor_target > 0.02]

# Collect the names of the features
names = highly_correlated_features.index.tolist()

# Display the results
print("Highly correlated features:")
print(names)

# Evaluate the model with new features
strong_features_eval_df = evaluate_model_on_features(X[names], Y)
strong_features_eval_df.index = ['Strong features']

# Append to results and display
results = pd.concat([results, strong_features_eval_df], ignore_index=True)
results.head()

def univariate_selection():
    """
    Performs univariate feature selection using the SelectKBest method with the f-classif scoring function.

    Args:
        X: The feature matrix.
        Y: The target variable.

    Returns:
        A list of feature names selected by the univariate selection process.
    """

    # Split train and test sets
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=123)

    # Normalize all features of the train and test datasets
    scaler = StandardScaler().fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Select top 5 features based on f-test
    selector = SelectKBest(f_classif, k=5)

    # Fit to scaled data, then transform it
    X_new = selector.fit_transform(X_train_scaled, Y_train)

    # Get selected feature indices
    feature_idx = selector.get_support()

    # Print the results
    for name, included in zip(X.columns, feature_idx):
        print("%s: %s" % (name, included))

    # Extract selected feature names
    feature_names = X.columns[feature_idx]

    return feature_names

univariate_feature_names = univariate_selection()

# Calculate and check model metrics
univariate_eval_df = evaluate_model_on_features(X, Y)
univariate_eval_df.index = ['F-test']

# Append to results and display
results = pd.concat([results, univariate_eval_df], ignore_index=True)
results.head(n=10)

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel

def feature_importances_from_tree_based_model(X, Y, test_size=0.2, random_state=123):
    """
    Calculates feature importances from a Random Forest Classifier model.

    Args:
        X (pandas.DataFrame): The input features.
        Y (pandas.Series): The target variable.
        test_size (float, optional): The proportion of data to use for the test set. Defaults to 0.2.
        random_state (int, optional): Seed for random number generation. Defaults to 123.

    Returns:
        sklearn.ensemble.RandomForestClassifier: The fitted Random Forest Classifier model.
        pandas.Index: The feature names.
    """

    # Split train and test set
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size, stratify=Y, random_state=random_state)

    # Standardize features (assuming numerical features)
    scaler = StandardScaler().fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Define and fit the Random Forest Classifier model
    model = RandomForestClassifier(random_state=random_state)
    model.fit(X_train_scaled, Y_train)

    # Plot feature importance
    plt.figure(figsize=(12, 8))  # Increase figure size for better readability
    feat_importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
    feat_importances.plot(kind='barh', color='teal')  # Use a modern color for bars

    plt.xlabel("Feature Importance")
    plt.ylabel("Feature")
    plt.title("Feature Importances from Random Forest Classifier", fontsize=16, weight='bold')
    plt.grid(axis='x', linestyle='--', alpha=0.6)  # Add grid lines for better visualization

    # Annotate bars with importance values
    for index, value in enumerate(feat_importances):
        plt.text(value + 0.01, index, f"{value:.3f}", va='center', fontsize=10, color='black', weight='bold')

    plt.tight_layout()
    plt.show()

    return model, X.columns

def select_features_from_model(model, feature_names, threshold=0.013):
    """
    Selects features based on importance from a fitted model.

    Args:
        model (sklearn.base.Transformer): The fitted model from which to select features.
        feature_names (pandas.Index): The names of the features.
        threshold (float, optional): The minimum importance threshold for feature selection. Defaults to 0.013.

    Returns:
        list: A list of selected feature names.
    """

    selector = SelectFromModel(model, prefit=True, threshold=threshold)
    feature_idx = selector.get_support()
    feature_names_selected = feature_names[feature_idx]

    return feature_names_selected

# Assuming you have your data in X and Y variables
model, feature_names = feature_importances_from_tree_based_model(X, Y)
selected_feature_names = select_features_from_model(model, feature_names)

print("Selected features based on importance threshold (0.013):")
print(selected_feature_names)

def run_rfe():

    # Split train and test sets
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2,stratify=Y, random_state = 123)

    # All features of dataset are float values. You normalize all features of the train and test dataset here.
    scaler = StandardScaler().fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Define the model
    model = RandomForestClassifier(criterion='entropy', random_state=47)

    # Wrap RFE around the model
    rfe = RFE(model, n_features_to_select=20)

    # Fit RFE
    rfe = rfe.fit(X_train_scaled, Y_train)
    feature_names = X.columns[rfe.get_support()]

    return feature_names

rfe_feature_names = run_rfe()

# Calculate and check model metrics
rfe_eval_df = evaluate_model_on_features(X[rfe_feature_names], Y)
rfe_eval_df.index = ['RFE']

# Append to results and display
results = pd.concat([results, rfe_eval_df], ignore_index=True)
results.head(n=10)

# Calculate and check model metrics
feat_imp_eval_df = evaluate_model_on_features(X[feature_imp_feature_names], Y)
feat_imp_eval_df.index = ['Feature Importance']

# Append to results and display
results = pd.concat([results, rfe_eval_df], ignore_index=True)
results.head(n=10)

def run_l1_regularization():

    # Split train and test set
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2,stratify=Y, random_state = 123)

    # All features of dataset are float values. You normalize all features of the train and test dataset here.
    scaler = StandardScaler().fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Select L1 regulated features from LinearSVC output
    selection = SelectFromModel(LinearSVC(C=1, penalty='l1', dual=False))
    selection.fit(X_train_scaled, Y_train)

    feature_names = X.columns[(selection.get_support())]

    return feature_names

l1reg_feature_names = run_l1_regularization()

# TENSORFLOW -DL

import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization, Activation, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import joblib
import matplotlib.pyplot as plt

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

model = Sequential([
    # Input layer: 128 neurons, accepting input shape (number of features)
    Dense(128, input_shape=(X_train_split.shape[1],)),
    # Batch normalization to standardize inputs
    BatchNormalization(),
    # ReLU activation function for non-linearity
    Activation('relu'),
    # Dropout for regularization, preventing overfitting
    Dropout(0.2),

    # Hidden layer 1: 256 neurons
    Dense(256),
    BatchNormalization(),
    Activation('relu'),
    Dropout(0.5),

    # Hidden layer 2: 64 neurons
    Dense(64),
    BatchNormalization(),
    Activation('relu'),
    Dropout(0.2),

    # Hidden layer 3: 16 neurons
    Dense(16),
    BatchNormalization(),
    Activation('relu'),
    Dropout(0.1),

    # Output layer: 1 neuron, sigmoid activation for binary classification
    Dense(1, activation='sigmoid')
])

model.compile(
    loss='binary_crossentropy',
    optimizer='RMSprop',
    metrics=['accuracy']
)

# Define EarlyStopping
early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=5,
    verbose=1
)

# Train the model using the early stopping callback
history = model.fit(
    X_train,
    y_train,
    validation_data=(X_val, y_val),
    epochs=20,
    batch_size=32,
    callbacks=[early_stopping]
)

# 5. Evaluate Model
val_preds = (model.predict(X_val) > 0.5).astype("int32")
print("Classification Report on Validation Data:\n", classification_report(y_val, val_preds))

# 6. Make Predictions
test_preds = (model.predict(X_test[:len(test)]) > 0.5).astype("int32")

test['Prediction'] = test_preds

# Save predictions to CSV
test[['UID', 'Prediction']].to_csv('predictions.csv', index=False)

import sklearn.preprocessing

#save the model for future use
model.save('model.h5')

# Import libraries (assumed)
import matplotlib.pyplot as plt

# Function to plot training history
def plot_history(history):
  """
  This function takes a 'history' object, typically generated by fitting a model
  using libraries like Keras or TensorFlow, and plots the training and validation
  accuracy and loss curves.

  Args:
      history: A dictionary containing the training history. It should have keys
               like 'accuracy', 'val_accuracy', 'loss', and 'val_loss'.
  """

  # Configure the figure size
  plt.figure(figsize=(18, 8))  # Adjust the figure size for better readability

  # Accuracy subplot
  plt.subplot(1, 2, 1)  # Create a subplot occupying 1 row, 2 columns, position 1

  # Plot training and validation accuracy
  plt.plot(history.history['accuracy'], label='Training accuracy')
  plt.plot(history.history['val_accuracy'], label='Validation accuracy')

  # Set labels and title
  plt.xlabel('Epoch')
  plt.ylabel('Accuracy')
  plt.legend(loc='lower right')  # Place the legend in the lower right corner
  plt.title('Training and Validation Accuracy')
  plt.grid(True)  # Add grid lines for better visualization

  # Loss subplot
  plt.subplot(1, 2, 2)  # Create a subplot occupying 1 row, 2 columns, position 2

  # Plot training and validation loss
  plt.plot(history.history['loss'], label='Training loss')
  plt.plot(history.history['val_loss'], label='Validation loss')

  # Set labels and title
  plt.xlabel('Epoch')
  plt.ylabel('Loss')
  plt.legend(loc='upper right')  # Place the legend in the upper right corner
  plt.title('Training and Validation Loss')
  plt.grid(True)  # Add grid lines for better visualization

  # Display the plot
  plt.show()

plot_history(history)



