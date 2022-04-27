import pandas as pd
from sklearn.model_selection import train_test_split
from supervised.automl import AutoML

X_train = pd.read_csv('X_train.csv')
y_train = pd.read_csv('y_train.csv')


# automl = AutoML(mode="Compete", results_path="ml_models", explain_level=2, total_time_limit=60 * 60 * 3)
# automl.fit(X_train, y_train)

automl_1 = AutoML()
automl_1.fit(X_train, y_train)

automl = AutoML(results_path="AutoML_classifier")
automl.fit(X_train, y_train)

# train models with AutoML
automl = AutoML(mode="Explain")
automl.fit(X_train, y_train)

automl = AutoML(algorithms=["Decision Tree"], start_random_models=3)
automl.fit(X_train, y_train)