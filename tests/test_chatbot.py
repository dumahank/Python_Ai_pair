import pytest
from chatbot import categorize_input, respond, user_history


def test_categorize_greeting():
    cat, info = categorize_input('Hello')
    assert cat == 'greeting'
    assert info is None


def test_categorize_question_known():
    cat, info = categorize_input('What is your name?')
    assert cat == 'question'
    assert isinstance(info, str)
    assert 'Rule-Based ChatBot' in info


def test_categorize_farewell():
    cat, info = categorize_input('bye')
    assert cat == 'farewell'


def test_respond_follow_up_and_why():
    # Clear history
    user_history.clear()

    # Ask a known question
    resp1, cat1 = respond('What can you do?')
    assert cat1 == 'question'
    assert 'respond to greetings' in resp1 or 'I can respond' in resp1

    # Follow-up
    resp2, cat2 = respond('and why?')
    assert cat2 == 'question'
    assert 'programmed' in resp2


def test_respond_farewell():
    resp, cat = respond('goodbye')
    assert cat == 'farewell'
    assert 'Goodbye' in resp
