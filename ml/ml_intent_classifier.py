"""
Machine Learning Intent Classifier for YatriSetu Chatbot
Uses scikit-learn for lightweight, fast intent classification
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
import pickle
import json
import numpy as np

class IntentClassifier:
    """Lightweight ML intent classifier using TF-IDF + SVM"""
    
    def __init__(self):
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(
                ngram_range=(1, 2),
                max_features=1000,
                lowercase=True,
                stop_words='english'
            )),
            ('clf', SVC(
                kernel='linear',
                probability=True,
                C=1.0
            ))
        ])
        self.intent_labels = []
        self.is_trained = False
    
    def train(self, training_data_path):
        """Train intent classifier from JSON training data"""
        print(f"Loading training data from {training_data_path}...")
        
        with open(training_data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        X = []
        y = []
        
        for intent_data in data['intents']:
            intent = intent_data['intent']
            for example in intent_data['examples']:
                X.append(example.lower())
                y.append(intent)
        
        self.intent_labels = sorted(list(set(y)))
        
        print(f"Training on {len(X)} examples, {len(self.intent_labels)} intents...")
        print(f"Intents: {', '.join(self.intent_labels)}")
        
        # Train model
        self.model.fit(X, y)
        self.is_trained = True
        
        # Cross-validation score
        scores = cross_val_score(self.model, X, y, cv=5)
        print(f"Cross-validation accuracy: {scores.mean():.3f} (+/- {scores.std():.3f})")
        
        return scores.mean()
    
    def predict(self, text, threshold=0.6):
        """
        Predict intent with confidence score
        
        Args:
            text: User input text
            threshold: Minimum confidence threshold (0-1)
        
        Returns:
            (intent, confidence) or (None, confidence) if below threshold
        """
        if not self.is_trained:
            return None, 0.0
        
        text_lower = text.lower()
        intent = self.model.predict([text_lower])[0]
        proba = self.model.predict_proba([text_lower])[0]
        confidence = max(proba)
        
        if confidence < threshold:
            return None, confidence
        
        return intent, confidence
    
    def predict_top_k(self, text, k=3):
        """Get top k intent predictions with probabilities"""
        if not self.is_trained:
            return []
        
        text_lower = text.lower()
        proba = self.model.predict_proba([text_lower])[0]
        
        # Get top k indices
        top_k_idx = np.argsort(proba)[-k:][::-1]
        
        results = []
        for idx in top_k_idx:
            results.append({
                'intent': self.intent_labels[idx],
                'confidence': float(proba[idx])
            })
        
        return results
    
    def save(self, path):
        """Save trained model to disk"""
        if not self.is_trained:
            raise ValueError("Model not trained yet")
        
        model_data = {
            'model': self.model,
            'intent_labels': self.intent_labels,
            'is_trained': self.is_trained
        }
        
        with open(path, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"Model saved to {path}")
    
    def load(self, path):
        """Load trained model from disk"""
        with open(path, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data['model']
        self.intent_labels = model_data['intent_labels']
        self.is_trained = model_data['is_trained']
        
        print(f"Model loaded from {path}")
        print(f"Intents: {', '.join(self.intent_labels)}")

if __name__ == '__main__':
    # Test the classifier
    classifier = IntentClassifier()
    
    # Create sample training data
    sample_data = {
        "intents": [
            {
                "intent": "find_route",
                "examples": [
                    "Route from CP to Dwarka",
                    "How to reach Noida",
                    "Bus to Airport"
                ]
            },
            {
                "intent": "check_fare",
                "examples": [
                    "Fare from CP to Dwarka",
                    "How much to Airport",
                    "Price to Noida"
                ]
            }
        ]
    }
    
    with open('test_training_data.json', 'w') as f:
        json.dump(sample_data, f)
    
    classifier.train('test_training_data.json')
    
    # Test predictions
    test_queries = [
        "Show me route to Airport",
        "What's the cost to Dwarka",
        "How much for ticket to Noida"
    ]
    
    for query in test_queries:
        intent, confidence = classifier.predict(query)
        print(f"Query: {query}")
        print(f"Intent: {intent}, Confidence: {confidence:.3f}\n")
