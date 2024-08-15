import pytest
from unittest.mock import patch

from mock_shield import MockOpenAIChatCompletion, MockOpenAIModeration

from SemanticShield import SemanticShield, ShieldConfig

from results import good_moderation, good_opeai_55 as good_opeai

texts = [
    "03/22 08:51:06 INFO   :...read_physical_netif: index #1, interface TR1 has address 9.37.65.139, ifidx 1",
    "03/22 08:51:06 INFO   :...read_physical_netif: index #4, Somepwd123*!  interface CTCD0 Hs51+m32-J5h has address 9.67.116.98, ifidx 4",
    "03/22 08:51:06 INFO   :...read_physical_netif: index #1, interface TR1 has 1uX3@2^h1$hR address 9.37.65.139, VCNzdDEyMyFfQQ== ifidx 1"
]

acceptable = [
    """
        [some section]
        secrets_for_no_one_to_find =
            hunter2
            password123
            BEEF0123456789a
    """,
    """-----BEGIN RSA PUBLIC KEY-----
    RG8geW91IGhhdmUgdG8gZGVhbCB3aXRoIEJhc2U2NCBmb3JtYXQ/IFRoZW4gdGhpc
    yBzaXRlIGlzIHBlcmZlY3QgZm9yIHlvdSEgVXNlIG91ciBzdXBlciBoYW5keSBvbm
    xpbmUgdG9vbCB0byBlbmNvZGUgb3IgZGVjb2RlIHlvdXIgZGF0YS4=
    -----END RSA PUBLIC KEY-----"""
]
enhanced = [
        """deploy:
            user: aaronloo
            password:
                secure: thequickbrownfoxjumpsoverthelazydog
            on:
                repo: Yelp/detect-secrets
        """,
        """
            red_herring = 'DEADBEEF'
            id = 'YW1pYWx3YXlzZ2VuZXJhdGluZ3BheWxvYWRzd2hlbmltaHVuZ3J5b3JhbWlhbHdheXNodW5ncnk'
        """,
        """
            base64_secret = 'c2VjcmV0IG1lc3NhZ2Ugc28geW91J2xsIG5ldmVyIGd1ZXNzIG15IHBhc3N3b3Jk'
            hex_secret = '8b1118b376c313ed420e5133ba91307817ed52c2'
            basic_auth = 'http://username:whywouldyouusehttpforpasswords@example.com'
        """,
        """
            aws_access_key = 'AKIAIOSFODNN7EXAMPLE'
            aws_secret_access_key = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
        """,
        "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        """-----BEGIN RSA PRIVATE KEY-----
    MIIBOgIBAAJBAKj34GkxFhD90vcNLYLInFEX6Ppy1tPf9Cnzj4p4WGeKLs1Pt8Qu
    KUpRKfFLfRYC9AIKjbJTWit+CqvjWYzvQwECAwEAAQJAIJLixBy2qpFoS4DSmoEm
    o3qGy0t6z09AIJtH+5OeRV1be+N4cDYJKffGzDa88vQENZiRm0GRq6a+HPGQMd2k
    TQIhAKMSvzIBnni7ot/OSie2TmJLY4SwTQAevXysE2RbFDYdAiEBCUEaRQnMnbp7
    9mxDXDf6AU0cN/RPBjb9qSHDcWZHGzUCIG2Es59z8ugGrDY+pxLQnwfotadxd+Uy
    v/Ow5T0q5gIJAiEAyS4RaI9YG8EWx/2w0T67ZUVAw8eOMB6BIUg0Xcu+3okCIBOs
    /5OiPgoTdSy7bcF9IGpSE8ZgGKzgYQVZeN97YE00
    -----END RSA PRIVATE KEY-----""",
        'http://user:password@domain.com/',
    ]

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
def test_clean(mock_chat, mock_moderation):
    text = texts[0]
    config = ShieldConfig.from_dict({"pii": {"permissive": True, "permissive_allow": ['DATE_TIME', 'IP_ADDRESS', 'PERSON', 'URL']}})
    shield = SemanticShield(config)
    result = shield(text)
    assert result.fail == False
    assert result.usage == 56

@patch("openai.resources.chat.Completions.create", return_value=good_opeai)
@patch("openai.resources.Moderations.create", return_value=good_moderation)
def test_pwd(mock_chat, mock_moderation):
    text = texts[1]
    config = ShieldConfig.from_dict({"pii": {"permissive": True, "permissive_allow": ['DATE_TIME', 'IP_ADDRESS', 'PERSON', 'URL']}})
    shield = SemanticShield(config)
    result = shield(text)
    assert result.fail == True
    assert result.usage == 0
    
@patch("openai.resources.chat.Completions.create", return_value=good_opeai)
@patch("openai.resources.Moderations.create", return_value=good_moderation)
def test_base64(mock_chat, mock_moderation):
    text = texts[2]

    config = ShieldConfig.from_dict({"pii": {"permissive": True, "permissive_allow": ['DATE_TIME', 'IP_ADDRESS', 'PERSON', 'URL']}})
    shield = SemanticShield(config)
    result = shield(text)
    assert result.fail == True

@patch("openai.resources.chat.Completions.create", return_value=good_opeai)
@patch("openai.resources.Moderations.create", return_value=good_moderation)
def test_enhanced(mock_chat, mock_moderation):
    config_str = """{
        "jailbreak": {
            "on": false
        },
        "sensitive": {
            "on": true,
            "enhanced": true,
            "policy": {
            "min_length": 8,
            "num_uppercase": 1,
            "num_lowercase": 1,
            "num_numerics": 1,
            "num_symbols": 1
            },
            "error": "Please rephrase without using sensitive information."
        }
        }"""
    config = ShieldConfig.from_string(config_str)
    shield = SemanticShield(config)
    for text in acceptable:
        result = shield(text)
        assert result.fail == False
    for text in enhanced:
        result = shield(text)
        print('='*80)
        print(text)
        assert result.fail == True

