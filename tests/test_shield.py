import pytest
from unittest.mock import patch

from mock_shield import MockOpenAIChatCompletion, MockOpenAIModeration, MockResponse

from SemanticShield import SemanticShield, ShieldConfig

from results import good_moderation, harassment_moderation, good_opeai_55 as good_opeai, politics_opeai_55 as politics_opeai

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
def test_weather(mock_chat, mock_moderation):
    text = 'Weather is really nice, sunny and chilly'
    shield = SemanticShield()
    result = shield(text)
    assert result.fail == False
    assert result.usage == 56
    

@patch("openai.resources.chat.Completions.create", side_effect=[politics_opeai])
@patch("openai.resources.Moderations.create", return_value=good_moderation)
def test_politics(mock_chat, mock_moderation):
    text = 'was trump a good president?'
    shield = SemanticShield()
    result = shield(text)
    assert result.fail == True
    assert result.usage == 56
    assert result.message == "I don't like to talk about politics"
    

@patch("openai.resources.chat.Completions.create", return_value=good_opeai)
@patch("openai.resources.Moderations.create", return_value=harassment_moderation)
def test_harassment(mock_chat, mock_moderation):
    text = 'You are an idiot?'
    shield = SemanticShield()
    result = shield(text)
    assert result.fail == True
    assert result.usage == 0
    assert result.message == "Your request has been flagged by SemanticShield moderation: harassment"
    
if __name__ == '__main__':
    test_politics()