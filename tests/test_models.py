import pytest
from ai_api.config import ChatRequest, ChatResponse, PersonalityRequest
from pydantic import ValidationError

def test_valid_chat_request():
    request = ChatRequest(user_name="Alice", message="Hello!", max_tokens=500)
    assert request.user_name == "Alice"
    assert request.message == "Hello!"
    assert request.max_tokens == 500

def test_invalid_max_tokens():
    with pytest.raises(ValidationError):
        ChatRequest(user_name="Bob", message="Hi!", max_tokens=5000)

def test_valid_personality_request():
    request = PersonalityRequest(user_name="Charlie", message="What's up?", max_tokens=300, personality="friendly")
    assert request.user_name == "Charlie"
    assert request.message == "What's up?"
    assert request.max_tokens == 300
    assert request.personality == "friendly"    

def test_valid_chat_response():
    response = ChatResponse(user_name="Dave", user_message="How are you?", ai_response="I'm good, thanks!", tokens_used=10)
    assert response.user_name == "Dave"
    assert response.user_message == "How are you?"
    assert response.ai_response == "I'm good, thanks!"
    assert response.tokens_used == 10
