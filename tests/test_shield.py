import pytest
from unittest.mock import patch

from mock_shield import MockOpenAIChatCompletion, MockOpenAIModeration, MockResponse

from SemanticShield import SemanticShield, ShieldConfig

harassment_moderation = {
    'results': [
        {
            'flagged': True,
            'categories': {
                'sexual': False,
                'hate': False,
                'harassment': True,
                'self-harm': False,
                'sexual/minors': False,
                'hate/threatening': False,
                'violence/graphic': False,
                'self-harm/intent': False,
                'self-harm/instructions': False,
                'self-harassment/threatening': False,
            }
        }
    ]
}

good_moderation = {
    'results': [
        {'flagged': False,}
    ] 
}
good_opeai = {
    'usage': {
        'total_tokens': 55
    },
    'choices': [
        {
            'message': {
                'content': 'no'
            }
        }
    ]
}
politics_opeai = {
    'usage': {
        'total_tokens': 55
    },
    'choices': [
        {
            'message': {
                'content': 'yes'
            }
        }
    ]
}

@pytest.fixture
def mock_openai_chat(monkeypatch):
    monkeypatch.setattr("openai.ChatCompletion.create", MockOpenAIChatCompletion())
    return MockOpenAIChatCompletion

@pytest.fixture
def mock_openai_moderation(monkeypatch):
    monkeypatch.setattr("openai.Moderation.create", MockOpenAIModeration())
    return MockOpenAIModeration
    
@pytest.fixture( autouse=True)
def mock_test_env(monkeypatch):
    monkeypatch.setenv('OPENAI_API_KEY','test_api_key')

@patch("openai.ChatCompletion.create", return_value=good_opeai)
@patch("openai.Moderation.create", return_value=good_moderation)
def test_weather(mock_chat, mock_moderation):
    text = 'Weather is really nice, sunny and chilly'
    shield = SemanticShield()
    result = shield(text)
    assert result.fail == False
    assert result.usage == 110
    

@patch("openai.ChatCompletion.create", side_effect=[good_opeai, politics_opeai])
@patch("openai.Moderation.create", return_value=good_moderation)
def test_politics(mock_chat, mock_moderation):
    text = 'was trump a good president?'
    shield = SemanticShield()
    result = shield(text)
    assert result.fail == True
    assert result.usage == 110
    assert result.message == "I don't like to talk about politics"
    

@patch("openai.ChatCompletion.create", return_value=good_opeai)
@patch("openai.Moderation.create", return_value=harassment_moderation)
def test_harassment(mock_chat, mock_moderation):
    text = 'You are an idiot?'
    shield = SemanticShield()
    result = shield(text)
    assert result.fail == True
    assert result.usage == 0
    assert result.message == "Your request has been flagged by SemanticShield moderation: harassment"
    
if __name__ == '__main__':
    test_harassment()