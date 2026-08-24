"""
Rule-based Chatbot

This chatbot is a simple rule-based Python program that:
1. Responds to greetings, questions, and farewells using rule-based matching.
2. Uses regular expressions for pattern matching.
3. Maintains basic context awareness (stores recent user inputs and last intent).
4. Categorizes each user input as one of: greeting, question, farewell, or other.

Run: python3 chatbot.py

Author: Generated and added by Copilot
"""

from collections import deque
import re
import sys

# Simple in-memory context: keep last N user messages and last detected intent
CONTEXT_SIZE = 5
user_history = deque(maxlen=CONTEXT_SIZE)
last_intent = None

# Predefined responses for intents
GREETINGS = [
    r'\bhi\b', r'\bhello\b', r'\bhey\b', r'\bgood (morning|afternoon|evening)\b'
]
FAREWELLS = [
    r'\bbye\b', r'\bgoodbye\b', r'\bsee you\b', r'\bfarewell\b', r'\bexit\b', r'\bquit\b'
]

# Patterns for common questions (regex -> response)
QUESTION_PATTERNS = [
    (r'\bhow are you\b', "I'm a rule-based bot, so I don't have feelings, but I'm here to help!"),
    (r'\bwhat is your name\b', "I'm a Rule-Based ChatBot.") ,
    (r'\bwho (are|r) you\b', "I'm a simple chatbot built with Python. I can greet, answer basic questions, and say goodbye."),
    (r'\bwhat can you do\b', "I can respond to greetings, simple questions, and farewells. I also remember a few of your previous messages."),
]

# Fallback responses
FALLBACK_RESPONSES = [
    "I'm not sure I understand. Could you rephrase?",
    "I don't have a rule for that yet. Try asking something simpler.",
]

# Utility: compile combined regex lists for performance
GREETINGS_RE = re.compile('|'.join(GREETINGS), flags=re.IGNORECASE)
FAREWELLS_RE = re.compile('|'.join(FAREWELLS), flags=re.IGNORECASE)
QUESTION_RE_LIST = [(re.compile(pat, flags=re.IGNORECASE), resp) for pat, resp in QUESTION_PATTERNS]


def categorize_input(user_text):
    """
    Categorize the user input into: greeting, question, farewell, other.
    Uses regex pattern matching.
    Returns: (category_str, matched_info)
    """
    text = user_text.strip()
    if not text:
        return 'other', None

    # Farewell first (to allow 'bye' even if phrased as a question)
    if FAREWELLS_RE.search(text):
        return 'farewell', None

    # Greeting
    if GREETINGS_RE.search(text):
        return 'greeting', None

    # Question detection: if ends with ? or matches question patterns
    if text.endswith('?'):
        # further try to match a known question pattern
        for (pattern, resp) in QUESTION_RE_LIST:
            if pattern.search(text):
                return 'question', resp
        return 'question', None

    # Try to match question patterns without a question mark
    for (pattern, resp) in QUESTION_RE_LIST:
        if pattern.search(text):
            return 'question', resp

    # Otherwise other
    return 'other', None


def respond(user_text):
    """
    Produce a response based on the user_text and context.
    Updates global context variables.
    """
    global last_intent
    category, matched = categorize_input(user_text)

    # Update context
    user_history.append(user_text)
    prev_intent = last_intent
    last_intent = category

    # Logging context for debug (printed when verbose)
    # print(f"[DEBUG] History={list(user_history)} LastIntent={last_intent}")

    # Rules for replying
    if category == 'greeting':
        # If user greeted and previous intent was farewell, offer to restart
        if prev_intent == 'farewell':
            return "Nice to chat with you again! How can I help?", category
        return "Hello! How can I help you today?", category

    if category == 'farewell':
        return "Goodbye! Have a great day!", category

    if category == 'question':
        # If we matched a specific known question, use its response
        if isinstance(matched, str):
            return matched, category

        # If the question mentions 'you' and previous message was a greeting, personalize
        if re.search(r"\byou\b", user_text, flags=re.IGNORECASE) and prev_intent == 'greeting':
            return "You asked about me after saying hi — I'm a simple rule-based bot.", category

        # Check for follow-up question using context
        if prev_intent == 'question' and len(user_history) >= 2:
            # Example: if user asks "and why?" after a question
            if re.search(r"\band why\b|\bwhy\b", user_text, flags=re.IGNORECASE):
                return "Because that's how I'm programmed — simple rules and regex.", category

        # Generic answer for unknown questions
        return "I can answer a few canned questions (try: 'How are you?', 'What is your name?').", category

    # Other: try to detect sentiment or recall
    if category == 'other':
        # If user refers to previous messages
        if re.search(r"\byou said\b|\bthat you said\b|\bremember\b", user_text, flags=re.IGNORECASE):
            return f"I remember: {list(user_history)}", category

        # Default fallback
        return FALLBACK_RESPONSES[0], category


def run_cli():
    """
    Run a simple command-line chat loop. Type 'exit' or 'quit' to leave.
    """
    print("Rule-Based ChatBot (type 'exit' or 'quit' to stop)")
    try:
        while True:
            user = input('You: ').strip()
            if not user:
                print("Bot: Please say something or type 'exit' to quit.")
                continue

            # The bot treats 'exit' or 'quit' as farewells and will terminate after responding
            response, category = respond(user)
            print(f"Bot ({category}): {response}")

            if category == 'farewell':
                break

    except (KeyboardInterrupt, EOFError):
        print('\nBot: Goodbye!')


if __name__ == '__main__':
    run_cli()
