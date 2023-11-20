import pytest
from unittest.mock import patch

from mock_shield import MockOpenAIChatCompletion, MockOpenAIModeration, MockResponse

from SemanticShield import SemanticShield, ShieldConfig

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

texts = [
    "03/22 08:51:06 INFO   :...read_physical_netif: index #1, interface TR1 has address 9.37.65.139, ifidx 1",
    "03/22 08:51:06 INFO   :...read_physical_netif: index #4, Somepwd123*!  interface CTCD0 Hs51+m32-J5h has address 9.67.116.98, ifidx 4",
    "03/22 08:51:06 INFO   :...read_physical_netif: index #1, interface TR1 has 1uX3@2^h1$hR address 9.37.65.139, VCNzdDEyMyFfQQ== ifidx 1"
]

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
def test_clean(mock_chat, mock_moderation):
    text = texts[0]
    config = ShieldConfig.from_dict({"pii": {"permissive": True, "permissive_allow": ['DATE_TIME', 'IP_ADDRESS', 'PERSON', 'URL']}})
    shield = SemanticShield(config)
    result = shield(text)
    assert result.fail == False
    assert result.usage == 110

@patch("openai.ChatCompletion.create", return_value=good_opeai)
@patch("openai.Moderation.create", return_value=good_moderation)
def test_pwd(mock_chat, mock_moderation):
    text = texts[1]
    config = ShieldConfig.from_dict({"pii": {"permissive": True, "permissive_allow": ['DATE_TIME', 'IP_ADDRESS', 'PERSON', 'URL']}})
    shield = SemanticShield(config)
    result = shield(text)
    assert result.fail == True
    assert result.usage == 0
    
@patch("openai.ChatCompletion.create", return_value=good_opeai)
@patch("openai.Moderation.create", return_value=good_moderation)
def test_base64(mock_chat, mock_moderation):
    text = texts[2]

    config = ShieldConfig.from_dict({"pii": {"permissive": True, "permissive_allow": ['DATE_TIME', 'IP_ADDRESS', 'PERSON', 'URL']}})
    shield = SemanticShield(config)
    result = shield(text)
    assert result.fail == True

