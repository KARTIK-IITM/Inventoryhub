# This file contains the chatbot API integration code
# Add this to your Flask application

import os
import requests
from flask import Blueprint, request, jsonify

# Create a Blueprint for the chatbot routes
chatbot_bp = Blueprint('chatbot', __name__)

# Get API key from environment variable for security
# You'll need to set this in your environment or .env file
CHATBOT_API_KEY = os.environ.get('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')
CHATBOT_API_URL = os.environ.get('https://openrouter.ai/api/v1')  # Replace with your actual API URL

@chatbot_bp.route('/api/chatbot', methods=['POST'])
def process_chatbot_message():
    """
    Process a message sent to the chatbot and return a response
    """
    if not CHATBOT_API_KEY:
        return jsonify({"response": "Chatbot API key not configured. Please contact the administrator."}), 500
    
    # Get the message from the request
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"response": "No message provided"}), 400
    
    user_message = data['message']
    
    try:
        # Call the external chatbot API
        response = requests.post(
            CHATBOT_API_URL,
            json={
                "message": user_message,
                # Add any other parameters your chatbot API requires
            },
            headers={
                "Authorization": f"Bearer {CHATBOT_API_KEY}",
                "Content-Type": "application/json"
            },
            timeout=10  # Set a timeout to prevent hanging requests
        )
        
        # Check if the request was successful
        if response.status_code == 200:
            chatbot_response = response.json()
            # Adjust this based on your API's response format
            return jsonify({"response": chatbot_response.get("reply", "I'm not sure how to respond to that.")})
        else:
            # Log the error (you should implement proper logging)
            print(f"Chatbot API error: {response.status_code} - {response.text}")
            return jsonify({"response": "I'm having trouble understanding right now. Please try again later."}), 500
    
    except requests.exceptions.RequestException as e:
        # Log the exception
        print(f"Chatbot API request failed: {str(e)}")
        return jsonify({"response": "I'm having trouble connecting to my brain. Please try again later."}), 500
    
    except Exception as e:
        # Log any other exceptions
        print(f"Unexpected error in chatbot processing: {str(e)}")
        return jsonify({"response": "Something unexpected happened. Please try again later."}), 500

# Fallback response function if you want to implement some basic responses without the API
def get_fallback_response(message):
    """
    Generate a simple fallback response based on keywords in the message
    """
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['hello', 'hi', 'hey']):
        return "Hello! How can I help you with your inventory today?"
    
    elif any(word in message_lower for word in ['bye', 'goodbye']):
        return "Goodbye! Feel free to chat again if you need assistance."
    
    elif any(word in message_lower for word in ['inventory', 'stock']):
        return "I can help you manage your inventory. You can ask about stock levels, item details, or how to add new items."
    
    elif any(word in message_lower for word in ['help', 'support']):
        return "I'm here to help! You can ask me about inventory management, stock levels, or specific items."
    
    else:
        return "I'm not sure I understand. Could you rephrase your question about inventory management?"

