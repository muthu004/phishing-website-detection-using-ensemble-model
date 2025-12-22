"""
Flask Web App for Ensemble Phishing Detection
"""

from flask import Flask, render_template, request, jsonify
from predict_ensemble import EnsemblePredictor
import traceback
import numpy as np

app = Flask(__name__)

# Load model once at startup
print("Initializing ensemble model...")
try:
    predictor = EnsemblePredictor()
    print("Model ready!")
except Exception as e:
    print(f"Error loading model: {e}")
    predictor = None


def convert_to_native(obj):
    """Convert numpy types to native Python types"""
    if isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj


@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """Predict URL safety"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'Please enter a URL'}), 400
        
        # Add http if missing
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        # Make prediction
        result = predictor.predict(url)
        
        # Generate reasons
        reasons = generate_reasons(result, url)
        
        response = {
            'url': result['url'],
            'prediction': result['prediction'],
            'is_safe': result['prediction'] == 'Benign',
            'confidence': float(result['confidence']),
            'ensemble': {
                'benign': float(result['ensemble']['benign']),
                'phishing': float(result['ensemble']['phishing'])
            },
            'ml': {
                'benign': float(result['ml']['benign']),
                'phishing': float(result['ml']['phishing'])
            },
            'dl': {
                'benign': float(result['dl']['benign']),
                'phishing': float(result['dl']['phishing'])
            },
            'html_fetched': result['html_fetched'],
            'reasons': reasons
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


def generate_reasons(result, url):
    """Generate human-readable reasons for the prediction"""
    reasons = []
    
    # URL structure analysis
    if url.startswith('https://'):
        reasons.append({'type': 'positive', 'text': 'Uses secure HTTPS protocol'})
    else:
        reasons.append({'type': 'negative', 'text': 'Does not use secure HTTPS'})
    
    # URL length
    if len(url) > 75:
        reasons.append({'type': 'negative', 'text': f'Unusually long URL ({len(url)} characters)'})
    
    # Suspicious patterns
    suspicious_words = ['login', 'verify', 'account', 'update', 'secure', 'banking', 'paypal']
    found_words = [w for w in suspicious_words if w in url.lower()]
    if found_words:
        reasons.append({'type': 'negative', 'text': f'Contains suspicious words: {", ".join(found_words)}'})
    
    # IP address
    if any(part.replace('.', '').isdigit() for part in url.split('/')):
        reasons.append({'type': 'negative', 'text': 'May contain IP address instead of domain name'})
    
    # Multiple subdomains
    from urllib.parse import urlparse
    parsed = urlparse(url)
    domain = parsed.netloc
    subdomain_count = domain.count('.') - 1
    if subdomain_count > 2:
        reasons.append({'type': 'negative', 'text': f'Multiple subdomains detected ({subdomain_count})'})
    
    # Special characters
    if url.count('-') > 3:
        reasons.append({'type': 'negative', 'text': f'Excessive hyphens in URL ({url.count("-")})'})
    
    if '@' in url:
        reasons.append({'type': 'negative', 'text': 'Contains @ symbol (phishing technique)'})
    
    # Model agreement
    ml_phishing = result['ml']['phishing']
    dl_phishing = result['dl']['phishing']
    
    if abs(ml_phishing - dl_phishing) < 20:
        reasons.append({'type': 'info', 'text': 'Both ML and DL models agree on prediction'})
    else:
        reasons.append({'type': 'warning', 'text': 'Models show different confidence levels'})
    
    # HTML analysis
    if not result['html_fetched']:
        reasons.append({'type': 'warning', 'text': 'Could not analyze page content (HTML not accessible)'})
    else:
        reasons.append({'type': 'info', 'text': 'Full page content analyzed'})
    
    # Confidence level
    confidence = result['confidence']
    if confidence > 90:
        reasons.append({'type': 'info', 'text': f'Very high confidence ({confidence:.1f}%)'})
    elif confidence > 70:
        reasons.append({'type': 'info', 'text': f'High confidence ({confidence:.1f}%)'})
    else:
        reasons.append({'type': 'warning', 'text': f'Moderate confidence ({confidence:.1f}%) - exercise caution'})
    
    return reasons


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
