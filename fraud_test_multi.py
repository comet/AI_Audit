import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import recall_score, accuracy_score

# 1. Setup Environment
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("Fraud_Tree_Depth_Experiment")

# 2. Generate Data
X, y = make_classification(n_samples=1000, n_features=10, n_informative=8, random_state=123)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

# 3. Iterate over different "Tree Depths"
# We test depths from 1 (very simple) to 20 (very complex)
depths = [1, 2, 3, 5, 10, 20]

for depth in depths:
    with mlflow.start_run(run_name=f"depth_{depth}"):
        # Initialize and Train
        clf = DecisionTreeClassifier(max_depth=depth, random_state=42)
        clf.fit(X_train, y_train)
        
        # Performance on Training Data (How well it "studied")
        train_acc = accuracy_score(y_train, clf.predict(X_train))
        
        # Performance on Test Data (The "Final Exam")
        test_preds = clf.predict(X_test)
        test_acc = accuracy_score(y_test, test_preds)
        test_recall = recall_score(y_test, test_preds)
        
        # Log Parameters and Metrics
        mlflow.log_param("max_depth", depth)
        mlflow.log_metric("train_accuracy", train_acc)
        mlflow.log_metric("test_accuracy", test_acc)
        mlflow.log_metric("test_recall", test_recall)
        
        # Log the model
        mlflow.sklearn.log_model(clf, f"model_depth_{depth}")
        
        print(f"Run Finished: Depth {depth} | Train Acc: {train_acc:.2f} | Test Acc: {test_acc:.2f}")

print("\nAll runs complete. Open the MLflow UI to compare results.")