# 🛡️ Phishing Website Detection Using Ensemble Model(ML+DL)

A machine learning-based phishing website detection system that combines XGBoost and Bi-LSTM models in an ensemble approach for accurate real-time URL classification.

## 📋 Overview

This project implements an advanced phishing detection system that leverages both traditional machine learning (XGBoost) and deep learning (Bi-LSTM) models to identify malicious websites. The ensemble approach combines the strengths of both models to achieve higher accuracy and reliability.

### Key Features

- **Dual Model Architecture**: Combines XGBoost for URL feature analysis and Bi-LSTM for HTML content analysis
- **Real-time Detection**: Flask web application for instant URL verification
- **Ensemble Voting**: Weighted voting system that leverages predictions from both ML and DL models
- **Comprehensive Analysis**: Examines URL structure, suspicious patterns, and page content
- **Confidence Scoring**: Provides detailed confidence metrics for each prediction

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/muthu004/phishing-website-detection-using-ensemble-model.git
cd phishing-website-detection-using-ensemble-model
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Additional dependencies for the Flask app:
```bash
pip install flask tensorflow beautifulsoup4 requests
```

## 📁 Project Structure

```
phishing-website-detection-using-ensemble-model/
├── app.py                          # Flask web application
├── train_model.py                  # XGBoost model training script
├── train_ensemble.py               # Ensemble configuration
├── phishing-detection-dl.ipynb     # Deep learning model notebook
├── requirements.txt                # Project dependencies
├── .gitignore                      # Git ignore file
└── README.md                       # Project documentation
```

## 🎯 Usage

### Training the Models

#### 1. Train the ML Model (XGBoost)

```bash
python train_model.py
```

This will:
- Load the URL features dataset
- Train an XGBoost classifier
- Save the model as `url_model.pkl`
- Generate performance metrics

#### 2. Train the DL Model (Bi-LSTM)

Open and run the Jupyter notebook:
```bash
jupyter notebook phishing-detection-dl.ipynb
```

This notebook will:
- Process HTML content features
- Train a Bi-LSTM neural network
- Save the deep learning model

#### 3. Configure the Ensemble

```bash
python train_ensemble.py
```

This creates the ensemble configuration with equal weights (0.5 each) for both models.

### Running the Web Application

Start the Flask server:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

#### Using the Web Interface

1. Open your browser and navigate to `http://localhost:5000`
2. Enter a URL to check
3. View the prediction results including:
   - Overall verdict (Benign/Phishing)
   - Confidence score
   - Individual model predictions
   - Detailed analysis reasons

## 🔍 Detection Features

The system analyzes multiple aspects of URLs:

### URL-based Features
- Protocol security (HTTP vs HTTPS)
- URL length and complexity
- Presence of IP addresses
- Subdomain count
- Special characters (@, -, etc.)
- Suspicious keywords

### Content-based Features
- HTML structure analysis
- JavaScript presence
- Form elements
- External links
- Meta tags

### Model Predictions
- **ML Model**: Fast analysis of URL structural features
- **DL Model**: Deep analysis of page content and patterns
- **Ensemble**: Combined weighted prediction for final verdict

## 🛠️ Technology Stack

- **Machine Learning**: XGBoost, scikit-learn
- **Deep Learning**: TensorFlow/Keras (Bi-LSTM)
- **Web Framework**: Flask
- **Data Processing**: pandas, numpy
- **Web Scraping**: BeautifulSoup4, requests
- **Model Persistence**: joblib



