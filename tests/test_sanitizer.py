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
    assert result.pii_max == 1.0
    assert result.pii_total == 5.55

def test_permissive():
    config = ShieldConfig.from_dict({"pii": {"permissive": False}})
    shield = SemanticShield(config)

    result = shield(text)
    assert result.fail == True
    assert result.pii_max == 1.0
    assert result.pii_total == 5.55

def test_strict():
    config = ShieldConfig.from_dict({"pii": {"permissive": True}})
    shield = SemanticShield(config)

    result = shield.check_pii(text)
    assert result.fail == True
    assert result.pii_max == 1.0
    assert result.pii_total == 3.0

def test_text():
    config = ShieldConfig.from_dict({"pii": {"permissive": True, "use_placeholders": False}})
    shield = SemanticShield(config)
    result = shield.sanitize(text)
    assert result.fail == True
    assert result.sanitized.startswith("My name is Jason Bourne and my phone number is") == True

def test_use_placeholders():
    config = ShieldConfig.from_dict({"pii": {"permissive": False, "use_placeholders": True}})
    shield = SemanticShield(config)
    result = shield.sanitize(text)
    assert result.fail == True
    assert result.sanitized.startswith("My name is [PERSON 1] and my phone number is [PHONE_NUMBER 5].") == True

if __name__ == '__main__':
    test_default()