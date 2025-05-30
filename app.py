from flask import Flask, request, jsonify
from transformers import pipeline
import torch

app = Flask(__name__)

# Load emotion detection model
emotion_classifier = pipeline(
    "text-classification", 
    model="finiteautomata/bertweet-base-emotion-analysis",
    return_all_scores=True
)

@app.route('/detect-emotion', methods=['POST'])
def detect_emotion():
    data = request.get_json()
    text = data.get('text', '')
    
    # Get emotion predictions
    predictions = emotion_classifier(text)
    
    # Get the emotion with highest score
    top_emotion = max(predictions[0], key=lambda x: x['score'])
    emotion = top_emotion['label']
    
    # Generate response based on emotion (this is a simple example)
    responses = {
        'joy': f"I sense you're happy about this! That's wonderful!",
        'anger': "I notice some frustration in your words. Would you like to talk about it?",
        'sadness': "I detect some sadness. I'm here to listen if you need support.",
        'fear': "It seems there might be some concern here. You're not alone.",
        'surprise': "Wow, that's surprising! Tell me more.",
        'disgust': "I sense some strong disapproval. Would you like to elaborate?",
        'others': "Thank you for sharing. How can I assist you further?"
    }
    
    response_text = responses.get(emotion.lower(), responses['others'])
    
    return jsonify({
        'emotion': emotion,
        'response': response_text
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)