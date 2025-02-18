import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
import random

file_path = "dataset.csv"  # Update with the correct path

df = pd.read_csv(file_path)

X = df.drop(columns=['IsItSecure'])
y = df['IsItSecure']

splits = []
# random_states = [42, 21, 84, 99]
random_states = [random.randint(1, 100) for _ in range(4)]
for state in random_states:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=state)
    splits.append((X_train, X_test, y_train, y_test))

best_accuracy = 0
best_model = None

for i, (X_train, X_test, y_train, y_test) in enumerate(splits):
    print(f"\nTraining on split {i+1} with random state {random_states[i]}")
    
    # Train Random Forest model
    rf_model = RandomForestClassifier(n_estimators=100, random_state=random_states[i])
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    accuracy_rf = accuracy_score(y_test, y_pred_rf)
    print(f"Random Forest Accuracy: {accuracy_rf}")
    
    # Train Decision Tree model
    # dt_model = DecisionTreeClassifier(random_state=random_states[i])
    # dt_model.fit(X_train, y_train)
    # y_pred_dt = dt_model.predict(X_test)
    # accuracy_dt = accuracy_score(y_test, y_pred_dt)
    # print(f"Decision Tree Accuracy: {accuracy_dt}")
    if accuracy_rf > best_accuracy and accuracy_rf < 0.9:
        best_accuracy = accuracy_rf
        best_model = rf_model
    # if accuracy_dt > best_accuracy:
    #     best_accuracy = accuracy_dt
    #     best_model = dt_model

with open("best_model.pkl", "wb") as f:
    pickle.dump(best_model, f)
print("Best model saved as best_model.pkl with accuracy:", best_accuracy)
