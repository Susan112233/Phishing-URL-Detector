# Step 1: Import Libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import svm, tree
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
import matplotlib.pyplot as plt

# Step 2: Load Datasets
legitimate_df = pd.read_csv("structured_data_legitimate.csv")
phishing_df = pd.read_csv("structured_data_phishing.csv")

# Step 3: Combine and Shuffle Datasets
df = pd.concat([legitimate_df, phishing_df], axis=0).sample(frac=1).reset_index(drop=True)

# Step 4: Prepare Features (X) and Labels (y), Drop URL Column if Exists
df = df.drop(columns='URL', errors='ignore').drop_duplicates()
X = df.drop(columns='label')
y = df['label']

# Step 5: Train-Test Split for Initial Evaluation
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)

# Step 6: Initialize Models
svm_model = svm.LinearSVC(max_iter=10000)
rf_model = RandomForestClassifier(n_estimators=60)
dt_model = tree.DecisionTreeClassifier()
ab_model = AdaBoostClassifier()
nb_model = GaussianNB()
nn_model = MLPClassifier(alpha=1, max_iter=1000)
kn_model = KNeighborsClassifier()

models = {
    'Support Vector Machine': svm_model,
    'Random Forest': rf_model,
    'Decision Tree': dt_model,
    'AdaBoost': ab_model,
    'Gaussian Naive Bayes': nb_model,
    'Neural Network': nn_model,
    'K-Neighbors': kn_model
}

# Step 7: Initial Evaluation of Each Model on the Training/Test Split
print("Initial Model Evaluation on Test Set")
initial_metrics = {}
for name, model in models.items():
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    initial_metrics[name] = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, zero_division=0),
        'recall': recall_score(y_test, y_pred, zero_division=0)
    }
    print(f"{name} - Accuracy: {initial_metrics[name]['accuracy']:.4f}, "
          f"Precision: {initial_metrics[name]['precision']:.4f}, "
          f"Recall: {initial_metrics[name]['recall']:.4f}")

# Step 8: Prepare for Manual K-Fold Cross-Validation
K = 5
total = X.shape[0]
index = int(total / K)

# Step 9: Split Data into K Folds Manually
X_train_list = [
    X.iloc[index:], X.iloc[np.r_[:index, index*2:]], X.iloc[np.r_[:index*2, index*3:]],
    X.iloc[np.r_[:index*3, index*4:]], X.iloc[:index*4]
]
X_test_list = [
    X.iloc[:index], X.iloc[index:index*2], X.iloc[index*2:index*3],
    X.iloc[index*3:index*4], X.iloc[index*4:]
]
y_train_list = [
    y.iloc[index:], y.iloc[np.r_[:index, index*2:]], y.iloc[np.r_[:index*2, index*3:]],
    y.iloc[np.r_[:index*3, index*4:]], y.iloc[:index*4]
]
y_test_list = [
    y.iloc[:index], y.iloc[index:index*2], y.iloc[index*2:index*3],
    y.iloc[index*3:index*4], y.iloc[index*4:]
]

# Step 10: Perform Manual K-Fold Cross-Validation
metrics = {name: {'accuracy': [], 'precision': [], 'recall': []} for name in models.keys()}

print("\nPerforming K-Fold Cross-Validation...")
for i in range(K):
    print(f"Fold {i+1}/{K}")
    X_train, X_test = X_train_list[i], X_test_list[i]
    y_train, y_test = y_train_list[i], y_test_list[i]
    
    for name, model in models.items():
        # Train and Predict
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        # Calculate Metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        
        # Append Metrics for Each Fold
        metrics[name]['accuracy'].append(accuracy)
        metrics[name]['precision'].append(precision)
        metrics[name]['recall'].append(recall)

# Step 11: Calculate Average Metrics Across Folds
print("\nK-Fold Cross-Validation Average Metrics:")
avg_metrics = {name: {} for name in models.keys()}
for name, metric in metrics.items():
    avg_metrics[name]['accuracy'] = np.mean(metric['accuracy'])
    avg_metrics[name]['precision'] = np.mean(metric['precision'])
    avg_metrics[name]['recall'] = np.mean(metric['recall'])
    print(f"{name} - Average Accuracy: {avg_metrics[name]['accuracy']:.4f}, "
          f"Precision: {avg_metrics[name]['precision']:.4f}, Recall: {avg_metrics[name]['recall']:.4f}")

# Step 12: Visualize Metrics Using Bar Charts
data = {
    'accuracy': [avg_metrics[name]['accuracy'] for name in models.keys()],
    'precision': [avg_metrics[name]['precision'] for name in models.keys()],
    'recall': [avg_metrics[name]['recall'] for name in models.keys()]
}
index = list(models.keys())
df_results = pd.DataFrame(data=data, index=index)

# Plotting Metrics
#ax = df_results.plot.bar(rot=0, figsize=(12, 8))
#plt.title('Model Performance Comparison (Manual K-Fold Cross-Validation)')
#plt.ylabel('Score')
#plt.xlabel('Models')
#plt.tight_layout()
#plt.show()

# Step 13: Summary of Best Model
best_model_name = max(avg_metrics, key=lambda name: avg_metrics[name]['accuracy'])
print(f"\nThe model with the highest average accuracy is: {best_model_name} "
      f"with an average accuracy of {avg_metrics[best_model_name]['accuracy']:.4f}")
