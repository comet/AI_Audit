import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1. Setup MLflow Tracking
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("Credit_Fraud_Walkthrough")

# 2. Generate Synthetic Credit Data
# We create 1000 rows. Each row has 10 features (e.g., Transaction Amount, Distance from Home, etc.)
X_raw, y_raw = make_classification(
    n_samples=1000, 
    n_features=10, 
    n_informative=8, 
    n_classes=2, 
    random_state=123
)

# Convert to Pandas for easy viewing
feature_names = [f"feature_{i}" for i in range(10)]
df = pd.DataFrame(X_raw, columns=feature_names)
df['is_fraud'] = y_raw

# --- STEP-BY-STEP DATA PREVIEW ---
print("--- DATA PREVIEW ---")
print(f"Dataset Shape: {df.shape}")
print("\nFirst 5 Transactions (Features):")
print(df[feature_names].head())
print("\nFirst 5 Labels (0 = Legit, 1 = Fraud):")
print(df['is_fraud'].head())
print("--------------------\n")

# 3. Split data
X_train, X_test, y_train, y_test = train_test_split(X_raw, y_raw, test_size=0.2)

# 4. Start MLflow Run
with mlflow.start_run(run_name="Initial_Fraud_Test"):
    # Hyperparameters
    params = {"n_estimators": 100, "max_depth": 5}
    mlflow.log_params(params)
    
    # Train
    model = RandomForestClassifier(**params)
    model.fit(X_train, y_train)
    
    # Evaluate
    acc = accuracy_score(y_test, model.predict(X_test))
    
    # Log metrics and the model itself
    mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(model, "model")
    
    print(f"Training Complete. Accuracy: {acc:.4f}")
    print("Check http://localhost:5000 to see the logged results!")