from pytest import approx

from SemanticShield import SemanticShield, ShieldConfig

text_driver = "I live in Ontario and my driver's licence is A12345-67890-1234."
text_ohip = "my OHIP card is 1234-123-123-AA."
text_ca_bank_acct = "Please deposit to my checking account 12345-123-1234567."
text_ca_passport = "my travel document is HG123456."
text_ca_sin = "my social insurance # is 123-123-123. (TODO - match actual sin algorithm)"


def test_driver():
    config = ShieldConfig.from_dict({"pii": {"permissive": False, "operation": "tokenize"}})
    shield = SemanticShield(config)
    result = shield(text_driver)
    assert result.fail == True
    assert result.pii_max == approx(1.0)
    assert result.pii_total == approx(1.85)
    result = shield.sanitize(text_driver)
    assert result.sanitized == "I live in [LOCATION 1] and my driver's licence is [ON_DRIVER_LICENSE 0]."
    
def test_ohip():
    config = ShieldConfig.from_dict({"pii": {"permissive": False, "operation": "tokenize"}})
    shield = SemanticShield(config)
    result = shield(text_ohip)
    assert result.fail == True
    assert result.pii_max == approx(1.0)
    assert result.pii_total == approx(1.0)
    result = shield.sanitize(text_ohip)
    assert result.sanitized == "my OHIP card is [OHIP_CARD 0]."

def test_ca_passport():
    config = ShieldConfig.from_dict({"pii": {"permissive": False, "operation": "tokenize"}})
    shield = SemanticShield(config)
    result = shield(text_ca_passport)
    assert result.fail == True
    assert result.pii_max == approx(1.0)
    assert result.pii_total == approx(1.0)
    result = shield.sanitize(text_ca_passport)
    assert result.sanitized == "my travel document is [CA_PASSPORT 0]."

def test_ca_passport2():
    config = ShieldConfig.from_dict({"pii": {"permissive": False, "operation": "tokenize"}})
    shield = SemanticShield(config)
    result = shield.sanitize(text_ca_passport)
    assert result.sanitized.startswith("my travel document is")

def test_ca_sin():
    config = ShieldConfig.from_dict({"pii": {"permissive": False, "operation": "tokenize"}})
    shield = SemanticShield(config)
    result = shield(text_ca_sin)
    assert result.fail == True
    assert result.pii_max == approx(0.9)
    assert result.pii_total == approx(0.9)
    result = shield.sanitize(text_ca_sin)
    assert result.sanitized == "my social insurance # is [CA_SIN 0]. (TODO - match actual sin algorithm)"

def test_ca_bank_acct():
    config = ShieldConfig.from_dict({"pii": {"permissive": False, "operation": "tokenize"}})
    shield = SemanticShield(config)
    result = shield(text_ca_bank_acct)
    assert result.fail == True
    assert result.pii_max == approx(1.0)
    assert result.pii_total == approx(1.0)
    result = shield.sanitize(text_ca_bank_acct)
    assert result.sanitized == "Please deposit to my checking account [CA_BANK_ACCT 0]."

if __name__ == '__main__':    
    test_driver()
    test_ohip()
    test_ca_passport()
    test_ca_passport2()