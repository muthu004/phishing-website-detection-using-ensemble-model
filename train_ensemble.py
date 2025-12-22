"""
Ensemble Model Training
Combines ML (XGBoost) and DL (Bi-LSTM) predictions for improved accuracy
"""

import json
class EnsembleModel:
    
    def __init__(self, ml_weight=0.5, dl_weight=0.5):
        
   
        self.ml_weight = ml_weight
        self.dl_weight = dl_weight
        
    def predict(self, ml_proba, dl_proba):
        """
        Combine predictions from both models
        ml_proba: probability from ML model (benign probability)
        dl_proba: probability from DL model (phishing probability)
        
        Returns: final prediction (0=benign, 1=phishing) and confidence
        """
        # Convert ML benign probability to phishing probability
        ml_phishing_proba = 1 - ml_proba
        
        # Weighted average
        ensemble_phishing_proba = (
            self.ml_weight * ml_phishing_proba + 
            self.dl_weight * dl_proba
        )
        
        # Threshold at 0.5
        prediction = 1 if ensemble_phishing_proba > 0.5 else 0
        confidence = ensemble_phishing_proba if prediction == 1 else (1 - ensemble_phishing_proba)
        
        return prediction, confidence, ensemble_phishing_proba


def save_ensemble_config():
    """Save ensemble configuration"""
    config = {
        'ml_weight': 0.5,
        'dl_weight': 0.5,
        'description': 'Equal weight ensemble of XGBoost and Bi-LSTM models',
        'threshold': 0.5
    }
    
    with open('ensemble_config.json', 'w') as f:
        json.dump(config, f, indent=4)
    
    print("\n" + "="*60)
    print("ENSEMBLE MODEL CONFIGURATION")
    print("="*60)
    print(f"ML Model Weight: {config['ml_weight']}")
    print(f"DL Model Weight: {config['dl_weight']}")
    print(f"Voting Strategy: Weighted Average")
    print(f"Threshold: {config['threshold']}")
    print("\nConfiguration saved to 'ensemble_config.json'")
    print("="*60)


if __name__ == "__main__":
    save_ensemble_config()
    
    print("\n✓ Ensemble model configured successfully!")
    print("\nThe ensemble combines:")
    print("  1. ML Model (XGBoost): Fast, accurate on URL features")
    print("  2. DL Model (Bi-LSTM): Deep analysis of HTML content")
    print("\nBoth models vote with equal weight for final prediction.")
    print("\nUse 'predict_ensemble.py' to make predictions with the ensemble.")
