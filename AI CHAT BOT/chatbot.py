# chatbot.py
import json
import random
import re
from datetime import datetime
from fuzzywuzzy import fuzz

class Chatbot:
    """
    A rule-based chatbot that uses a JSON file for its intents.
    It supports regex and fuzzy string matching, as well as dynamic data insertion.
    """
    def __init__(self, intents_file):
        """
        Initializes the chatbot by loading intents from a JSON file.
        :param intents_file: Path to the intents JSON file.
        """
        self.intents = self._load_intents(intents_file)

    def _load_intents(self, intents_file):
        """
        Loads the intents from the specified JSON file.
        :param intents_file: Path to the intents JSON file.
        :return: A list of intent objects.
        """
        try:
            with open(intents_file, 'r') as f:
                return json.load(f)['intents']
        except FileNotFoundError:
            print(f"Error: The file '{intents_file}' was not found.")
            return []
        except json.JSONDecodeError:
            print(f"Error: The file '{intents_file}' is not a valid JSON.")
            return []

    def _get_best_match(self, user_input):
        """
        Finds the best matching intent for the user's input.
        It prioritizes direct regex matches over fuzzy matches.
        :param user_input: The user's message.
        :return: A tuple of (best_matching_intent, match_score).
        """
        best_match_score = 0
        best_intent = None

        # First, check for an exact regex match
        for intent in self.intents:
            for pattern in intent['patterns']:
                if re.search(pattern, user_input, re.IGNORECASE):
                    # Found an exact regex match, return it with a perfect score
                    return intent, 100

        # If no regex match, use fuzzy matching
        for intent in self.intents:
            for pattern in intent['patterns']:
                # Calculate the fuzzy match ratio
                score = fuzz.token_set_ratio(user_input.lower(), pattern.lower())
                
                # Update the best match if the current score is higher
                if score > best_match_score:
                    best_match_score = score
                    best_intent = intent

        return best_intent, best_match_score

    def _get_dynamic_response(self, response_text):
        """
        Replaces dynamic placeholders in the response text with real-time data.
        Supported placeholders: {{date}}, {{time}}.
        :param response_text: The bot's response template.
        :return: The formatted response string.
        """
        current_datetime = datetime.now()
        
        # Replace date placeholder
        if '{{date}}' in response_text:
            response_text = response_text.replace('{{date}}', current_datetime.strftime("%A, %B %d, %Y"))
        
        # Replace time placeholder
        if '{{time}}' in response_text:
            response_text = response_text.replace('{{time}}', current_datetime.strftime("%I:%M %p"))
        
        return response_text

    def get_response(self, user_input):
        """
        Determines the bot's response to the user's input.
        :param user_input: The message from the user.
        :return: The bot's response as a string.
        """
        best_intent, match_score = self._get_best_match(user_input)

        # Check if the match is good enough (e.g., score > 75)
        if best_intent and match_score > 75:
            # Select a random response from the best-matched intent
            response_text = random.choice(best_intent['responses'])
            
            # Insert dynamic data if needed
            final_response = self._get_dynamic_response(response_text)
            return final_response
        else:
            # Fallback response for when no good match is found
            return "I'm sorry, I don't quite understand. Can you rephrase that?"

# Example of how to use the chatbot (for testing outside of Streamlit)
if __name__ == '__main__':
    bot = Chatbot('intents.json')
    print("Bot: Hi, I'm a simple chatbot. What can I do for you?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Bot: Goodbye!")
            break
        response = bot.get_response(user_input)
        print("Bot:", response)
