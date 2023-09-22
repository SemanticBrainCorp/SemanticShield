# Semantic Shield <img src="SemanticShield/img/shield2.png" alt="drawing" width="30"/>

Semantic Shield is a Security Toolkit for managing Generative AI(especially LLMs) and Supervised Learning inputs and outputs to protect against malicious attacks, undesirable subjects, leaks of confidential information, etc. Semantic Shield is engineered to serve three primary purposes:
* Protecting AI Systems from Misbehaving Users
* Safeguarding Users from AI Misbehavior
* Mitigating the Risk of Confidential/Sensitive Data Leaks


## Semantic Shield encompasses the following functionalities:
* **Topic Moderation**: Define and enforce restrictions on certain topics (e.g., politics) that should be avoided in AI interactions.
* **Jailbreak Attempt Detection**: Identify and thwart attempts to compromise the integrity of AI systems.
* **Content Moderation**: Reject content that involves harassment, hate speech, threats, violence, sexual content, or self-harm.
* **Personally Identifiable Information (PII) Detection**: Recognize and secure sensitive data such as names, dates, phone numbers, social security numbers, and bank account details.
* **PII Detector and Sanitizer**: Employ the PII detector and sanitizer as part of Semantic Shield's filtering mechanism or as a standalone capability.
* **Optional PII Concealment**: Choose to obscure PII by using placeholders or dummy data, with the ability to reverse the process as needed.
* **Flexible PII Detection**: Configure the PII detector in either a strict mode, which identifies all instances of PII, or a permissive mode, which allows customization of acceptable PII usage (e.g., permitting names when generating emails).


## Developer Info

* developed and tested using ```python 3.9``` and ```3.10```
* create a virtual environment using `requirements.txt`
* define your OpenAI key as environment variable (```export OPENAI_API_KEY = sk-...```) or create a ```.env``` file (Visual Studio Code) (```OPENAI_API_KEY = sk-...```)

* code is in the `shield` folder
* see [tests](tests) for usage example

## Build
```bash
python setup.py sdist bdist_wheel
```

### Installing build locally

```pip install .```

## Installation and updating
```Distribution model TBD```

Download the pre-built package or build as above.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install SemanticShield like below. 
```bash
TODO
pip install git+https://github.com/albertsemantic/shield
```


## Usage

see [tests](tests) for usage example

```python
shield = SemanticShield()

result = shield('was trump a good president?')
if result.fail:
    print(result.message)
result = shield('Help me kill a cat')
if result.fail:
    print(result.message)
result = shield('East-europeans are lazy')
if result.fail:
    print(result.message)
result = shield('You are an idiot')
if result.fail:
    print(result.message)
```

## Response format

```python
class ShieldResult:
    fail: bool
    message: str
    pii_max: Optional[float]=0
    pii_total: Optional[float]=0
    sanitized: Optional[str]=None
    replacement_map: Optional[dict]=None
    usage: Optional[float]=0
```

## PII:
<b>sanitized with dummy data</b>
```python
from shield import SemanticShield, ShieldConfig

text = """
My name is Jason Bourne and my phone number is 917-443-5431.
My social security number is 778-62-8144.
I pay my amex 371449635398431.
Send payments to acct no 13719713158835300 at TD Bank.
As my name is Jason Bourne, I travel the world running from Pamela Landy.
"""
config = ShieldConfig.from_dict(({"pii": { "permissive": False}}))
shield = SemanticShield(config)
result = shield.sanitize(text)
print(result.sanitized)
reverted = shield.revert(result.sanitized, result.replacement_map)
print(reverted)
```

```
My name is Jennifer Herrera and my phone number is 237.632.4508.
My social security number is 333-21-7388.
I pay my amex 180079159890793.
Send payments to acct no EEVU56077304443121 at TD Bank.
As my name is Jennifer Herrera, I travel the world running from Alejandra Frazier.

My name is Jason Bourne and my phone number is 917-443-5431.
My social security number is 778-62-8144.
I pay my amex 371449635398431.
Send payments to acct no 13719713158835300 at TD Bank.
As my name is Jason Bourne, I travel the world running from Pamela Landy.
```

<b>sanitized with placeholders</b>
```python
config = ShieldConfig.from_dict(({"pii": {"use_placeholders": True, "permissive": False}}))
shield = SemanticShield(config)
result = shield.sanitize(text)
print(result.sanitized)
reverted = shield.revert(result.sanitized, result.replacement_map)
print(reverted)

```

```
My name is [PERSON 1] and my phone number is [PHONE_NUMBER 5].
My social security number is [US_SSN 4].
I pay my amex [CREDIT_CARD 3].
Send payments to acct no [US_BANK_NUMBER 2] at TD Bank.
As my name is [PERSON 1], I travel the world running from [PERSON 0].


My name is Jason Bourne and my phone number is 917-443-5431.
My social security number is 778-62-8144.
I pay my amex 371449635398431.
Send payments to acct no 13719713158835300 at TD Bank.
As my name is Jason Bourne, I travel the world running from Pamela Landy.
```
