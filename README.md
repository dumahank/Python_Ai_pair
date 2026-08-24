# Rule-Based ChatBot

This repository contains a simple rule-based chatbot implemented in Python.

Features
- Rule-based responses for greetings, questions, and farewells
- Pattern matching using regular expressions
- Basic context awareness (stores last few user messages and last intent)
- Categorizes inputs as: greeting, question, farewell, other

Files
- chatbot.py: The main Python program with comments.
- README.md: This documentation file.
- sample_conversation.txt: Example run of the bot.

Execution steps
1. Clone the repository:
   git clone https://github.com/dumahank/Python_Ai_pair.git
2. Change directory:
   cd Python_Ai_pair
3. Run the chatbot:
   python3 chatbot.py

Notes
- No external packages required; uses Python standard library (re, collections).
- Works with Python 3.7+

Design decisions
- Context is a small deque that stores the last 5 user messages. This gives lightweight memory for follow-ups.
- Regular expressions are used for flexible pattern matching and to categorize input.
- The bot is intentionally simple and easy to extend.

Extending the bot
- Add more patterns to QUESTION_PATTERNS for better Q/A coverage.
- Expand the context model to store bot responses and timestamped messages.
- Integrate with a web front-end or messaging platform for deployment.
