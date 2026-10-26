
import os
import pickle
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Get the project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the new dataset
data_path = os.path.join(
    BASE_DIR, "data", "Crop_recommendation.csv"
)
df = pd.read_csv(data_path)

# Separate input features and target
X = df.drop("label", axis=1)
y = df["label"]

# Split the dataset while preserving crop proportions
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Create and train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)

print("Training completed!")
print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))
print("Number of crops:", len(model.classes_))
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save as a new file to preserve the old model for now
models_dir = os.path.join(BASE_DIR, "models")
os.makedirs(models_dir, exist_ok=True)

model_path = os.path.join(models_dir, "crop_model_v2.pkl")

with open(model_path, "wb") as file:
    pickle.dump(model, file)

print("\nNew model saved to:", model_path)
print("Input features:", list(X.columns))
print("Crop classes:", list(model.classes_))
