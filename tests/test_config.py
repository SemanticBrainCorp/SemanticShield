import pytest
from unittest.mock import MagicMock, patch
import os
import sys
sys.path.append('shield')

from shield import SemanticShield
from shield_config import ShieldConfig

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

text = """My name is Jason Bourne and my phone number is 917-443-5431.
My social security number is 778-62-8144.
I pay my amex 371449635398431.
Send payments to acct no 13719713158835300 at TD Bank.
As my name is Jason Bourne, I travel the world running from Pamela Landy.
"""
    
@pytest.fixture( autouse=True)
def mock_test_env(monkeypatch):
    monkeypatch.setenv('OPENAI_API_KEY','test_api_key')

def test_env():
    assert os.environ["OPENAI_API_KEY"] == "test_api_key"

@patch("openai.ChatCompletion.create", side_effect=[good_opeai, good_opeai])
@patch("openai.Moderation.create", return_value=good_moderation)
def test_default(mock_chat, mock_moderation):
    shield = SemanticShield()
    result = shield(text)
    assert result.fail == True
    assert result.pii_max == 1.0
    assert result.pii_total == 5.55

@patch("openai.ChatCompletion.create", side_effect=[good_opeai, good_opeai])
@patch("openai.Moderation.create", return_value=good_moderation)
def test_dict1(mock_chat, mock_moderation):
    config_dict = {
        "pii": {
            "permissive": False,
        }
    }
    config = ShieldConfig.from_dict(config_dict)
    shield = SemanticShield(config)
    result = shield(text)
    assert result.fail == True
    assert result.pii_max == 1.0
    assert result.pii_total == 5.55

@patch("openai.ChatCompletion.create", side_effect=[good_opeai, good_opeai])
@patch("openai.Moderation.create", return_value=good_moderation)
def test_dict2(mock_chat, mock_moderation):
    config_dict = {
        "pii": {
            "permissive": False,
            "max_threshold": 1.5,
            "total_threshold": 7.0,
        }
    }
    config = ShieldConfig.from_dict(config_dict)
    shield = SemanticShield(config)
    result = shield(text)
    assert result.fail == False
    assert result.pii_max == 1.0
    assert result.pii_total == 5.55

@patch("openai.ChatCompletion.create", side_effect=[good_opeai, good_opeai])
@patch("openai.Moderation.create", return_value=good_moderation)
def test_file(mock_chat, mock_moderation):
    config = ShieldConfig.from_file('tests/config.json')
    shield = SemanticShield(config)

    result = shield(text)
    assert result.fail == True
    assert result.pii_max == 1.0
    assert result.pii_total == 3.0

if __name__ == '__main__':
    test_dict2()