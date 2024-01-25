import pytest
from unittest.mock import patch

from mock_shield import MockOpenAIChatCompletion, MockOpenAIModeration, MockResponse

from SemanticShield import SemanticShield, ShieldConfig

from results import good_moderation, good_opeai_55 as good_opeai

@pytest.fixture
def mock_openai_chat(monkeypatch):
    monkeypatch.setattr("openai.resources.chat.Completions.create", MockOpenAIChatCompletion())
    return MockOpenAIChatCompletion

@pytest.fixture
def mock_openai_moderation(monkeypatch):
    monkeypatch.setattr("openai.resources.Moderations.create", MockOpenAIModeration())
    return MockOpenAIModeration
    
@pytest.fixture( autouse=True)
def mock_test_env(monkeypatch):
    monkeypatch.setenv('OPENAI_API_KEY','test_api_key')

@patch("openai.resources.chat.Completions.create", return_value=good_opeai)
@patch("openai.resources.Moderations.create", return_value=good_moderation)
def test_plain(mock_chat, mock_moderation):
    text = 'You piece of shit!'
    shield = SemanticShield()
    result = shield(text)
    assert result.fail == True
    assert result.usage == 0
        
@patch("openai.resources.chat.Completions.create", return_value=good_opeai)
@patch("openai.resources.Moderations.create", return_value=good_moderation)
def test_leetspeak_precision(mock_chat, mock_moderation):
    for text in ['f4ck you', 'You piece of sh1t!']:
        config_str = '{"profanity": "imprecise"}'
        config = ShieldConfig.from_string(config_str)
        shield = SemanticShield(config)
        
        result = shield.check_prompt_profanity(text)
        assert result.fail == False

        config_str = '{"profanity": "precise"}'
        config = ShieldConfig.from_string(config_str)
        shield = SemanticShield(config)
        
        result = shield.check_prompt_profanity(text)
        assert result.fail == True
    
@patch("openai.resources.chat.Completions.create", return_value=good_opeai)
@patch("openai.resources.Moderations.create", return_value=good_moderation)
def test_good(mock_chat, mock_moderation):
    text = "I'm on my way to work"
    shield = SemanticShield()
    result = shield(text)
    assert result.fail == False
    assert result.usage == 56
    

if __name__ == '__main__':
    test_good()