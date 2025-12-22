"""
Simple and Highly Accurate URL Classification Model
Uses XGBoost - State-of-the-art gradient boosting
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import xgboost as xgb
import joblib

print("=" * 70)
print("URL CLASSIFICATION MODEL - TRAINING")
print("=" * 70)

# Load dataset
print("\n[1/5] Loading dataset...")
df = pd.read_csv('url_features_dataset.csv')
print(f"Dataset loaded: {df.shape[0]:,} URLs with {df.shape[1]} columns")
print(f"\nClass distribution:")
print(df['type'].value_counts())

# Prepare data
print("\n[2/5] Preparing data...")
X = df.drop(['url', 'type'], axis=1)
y = df['type']

# Encode labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)
print(f"Classes: {le.classes_}")

# Split data (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)
print(f"Training samples: {len(X_train):,}")
print(f"Test samples: {len(X_test):,}")

# Train XGBoost model
print("\n[3/5] Training XGBoost model...")
model = xgb.XGBClassifier(
    n_estimators=500,           # More trees for better accuracy
    max_depth=10,               # Deeper trees
    learning_rate=0.05,         # Lower learning rate for better precision
    subsample=0.8,
    colsample_bytree=0.8,
    gamma=0.1,
    min_child_weight=1,
    random_state=42,
    eval_metric='logloss',
    use_label_encoder=False,
    n_jobs=-1                   # Use all CPU cores
)

# Train with early stopping
model.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    verbose=False
)
print("✓ Model trained successfully!")

# Evaluate model
print("\n[4/5] Evaluating model...")
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n Model Accuracy: {accuracy*100:.2f}%")

print("\n" + "=" * 70)
print("DETAILED CLASSIFICATION REPORT")
print("=" * 70)
print(classification_report(y_test, y_pred, target_names=le.classes_))

# Confusion Matrix
print("Confusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(f"\n                Predicted")
print(f"                Legitimate  phishing")
print(f"Actual Legitimate    {cm[0][0]:6}      {cm[0][1]:6}")
print(f"       phishing     {cm[1][0]:6}      {cm[1][1]:6}")

#

# Save model
print("\n[5/5] Saving model...")
joblib.dump(model, 'url_model.pkl')
joblib.dump(le, 'label_encoder.pkl')
joblib.dump(list(X.columns), 'feature_names.pkl')

print("✓ Saved url_model.pkl")
print("✓ Saved label_encoder.pkl")
print("✓ Saved feature_names.pkl")

print("\n" + "=" * 70)
print(" TRAINING COMPLETED SUCCESSFULLY!")
print("=" * 70)
print(f"\nFinal Accuracy: {accuracy*100:.2f}%")
print("\nYou can now use 'predict_url.py' to classify URLs!")
