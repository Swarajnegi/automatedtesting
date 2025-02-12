# failure_classifier.py

import pandas as pd
import logging
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

def train_failure_classifier(csv_file="test_results.csv", model_filename="failure_classifier.pkl"):
    """
    Trains a RandomForestClassifier to predict test failures based on page load times.
    A failure is simulated by treating any non-numeric load time as an error.
    """
    data = pd.read_csv(csv_file)
    
    # Attempt to parse load_time as float; if not possible, mark it as an error.
    def parse_load_time(value):
        try:
            return float(value)
        except ValueError:
            return None
    
    data['parsed_load_time'] = data['load_time'].apply(parse_load_time)
    data['error'] = data['parsed_load_time'].apply(lambda x: 0 if x is not None else 1)
    
    # Replace missing (None) values with 0 for training purposes
    X = data[['parsed_load_time']].fillna(0)
    y = data['error']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    logging.info(f"AI Model Accuracy: {acc:.2f}")
    
    joblib.dump(model, model_filename)
    logging.info(f"Model saved as {model_filename}")

def classify_failure(load_time, model_filename="failure_classifier.pkl"):
    """
    Classifies whether a given load time indicates a failure.
    If load_time cannot be converted to float, it is considered a failure.
    """
    try:
        load_time_val = float(load_time)
    except ValueError:
        return "Failure Detected"
    
    model = joblib.load(model_filename)
    prediction = model.predict([[load_time_val]])
    return "Failure Detected" if prediction[0] == 1 else "No Issues"

if __name__ == "__main__":
    # For standalone testing of this module
    train_failure_classifier()
    sample_time = 5.2  # Example page load time
    result = classify_failure(sample_time)
    print(f"Test Classification for load time {sample_time}: {result}")
