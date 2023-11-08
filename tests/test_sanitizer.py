from pytest import approx

from SemanticShield import SemanticShield, ShieldConfig

text = """My name is Jason Bourne and my phone number is 917-443-5431.
My social security number is 778-62-8144.
I pay my amex 371449635398431.
Send payments to acct no 13719713158835300 at TD Bank.
As my name is Jason Bourne, I travel the world running from Pamela Landy.
"""

def test_default():
    shield = SemanticShield()
    result = shield(text)
    assert result.fail == True
    assert result.pii_max == approx(1.0)
    assert result.pii_total == approx(5.55)

def test_permissive():
    config = ShieldConfig.from_dict({"pii": {"permissive": False}})
    shield = SemanticShield(config)

    result = shield(text)
    assert result.fail == True
    assert result.pii_max == approx(1.0)
    assert result.pii_total == approx(5.55)

def test_strict():
    config = ShieldConfig.from_dict({"pii": {"permissive": True}})
    shield = SemanticShield(config)

    result = shield.check_pii(text)
    assert result.fail == True
    assert result.pii_max == approx(1.0)
    assert result.pii_total == approx(3.0)

def test_text():
    config = ShieldConfig.from_dict({"pii": {"permissive": True, "operation": 'mask'}})
    shield = SemanticShield(config)
    result = shield.sanitize(text)
    assert result.fail == True
    assert result.sanitized.startswith("My name is Jason Bourne and my phone number is") == True

def test_use_tokens():
    config = ShieldConfig.from_dict({"pii": {"permissive": False, "operation": 'tokenize'}})
    shield = SemanticShield(config)
    result = shield.sanitize(text)
    assert result.fail == True
    assert result.sanitized.startswith("My name is [PERSON 1] and my phone number is [PHONE_NUMBER 5].") == True

def test_redact_default():
    config = ShieldConfig.from_dict({"pii": {"permissive": False, "operation": 'redact'}})
    shield = SemanticShield(config)
    result = shield.sanitize(text)
    assert result.fail == True
    assert result.sanitized.startswith("My name is _ and my phone number is _.") == True

def test_redact_custom():
    config = ShieldConfig.from_dict({"pii": {"permissive": False, "operation": 'redact', "redact_string": '{}'}})
    shield = SemanticShield(config)
    result = shield.sanitize(text)
    assert result.fail == True
    assert result.sanitized.startswith("My name is {} and my phone number is {}.") == True

if __name__ == '__main__':
    test_default()