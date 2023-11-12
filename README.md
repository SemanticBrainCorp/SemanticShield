# Semantic Shield <img src="https://raw.githubusercontent.com/SemanticBrainCorp/SemanticShield/main/SemanticShield/img/shield2.png" alt="Semantic Shield Logo" width="30"/>

Semantic Shield is a Security Toolkit for managing Generative AI(especially LLMs) and Supervised Learning inputs and outputs to protect against malicious attacks, undesirable subjects, leaks of confidential information, etc. Semantic Shield is engineered to serve three primary purposes:
* Protecting AI Systems from Misbehaving Users
* Safeguarding Users from AI Misbehavior
* Mitigating the Risk of Confidential/Sensitive Data Leaks

## NOTE
Semantic Shield represents an open-source initiative focused on AI security, safety, and alignment. Within this initiative, we have established a new direction to bring Semantic Shield in alignment with the best practices and tools of DevSecOps. This entails optimizing our efforts by:
1) Introducing identity/role-based access controls for AI services and resources 
2) Implementing output validation and recovery mechanisms as needed based on identity/role
3) Empowering DevSecOps personnel to effortlessly utilize and tailor Semantic Shield through the straightforward configuration of YAML files

## Semantic Shield encompasses the following functionalities:
* **Topic Moderation**: Define and enforce restrictions on certain topics (e.g., politics) that should be avoided in AI interactions.
* **Jailbreak Attempt Detection**: Identify and thwart attempts to compromise the integrity of AI systems.
* **Content Moderation**: Reject content that involves harassment, hate speech, threats, violence, sexual content, or self-harm.
* **Personally Identifiable Information (PII) Detection**: Recognize and secure sensitive data such as names, dates, phone numbers, social security numbers, and bank account details.
* **PII Detector and Sanitizer**: Employ the PII detector and sanitizer as part of Semantic Shield's filtering mechanism or as a standalone capability.
* **Optional PII Concealment**: Choose to obscure PII by using tokens or dummy data, with the ability to reverse the process as needed.
* **Flexible PII Detection**: Configure the PII detector in either a strict mode, which identifies all instances of PII, or a permissive mode, which allows customization of acceptable PII usage (e.g., permitting names when generating emails).


## Semantic Shield architecture and approach:

Semantic Shield offers two deployment options: integration as a library within an application or utilization as a service. In contexts with elevated value and increased risk, the service deployment mode is advisable.

Three principles driving architecture and approach are
* Network DMZ-Inspired Architecture
* Shift Left security
* Combining proven security best practices with AI innovation

[Learn more here](https://www.semanticbrain.net/post/semantic-shield-unleashed-open-source-initiative-for-ai-risk-mitigation)

![Semantic Brain Vision pptx (6)](https://github.com/SemanticBrainCorp/SemanticShield/assets/1478133/bda4b456-6250-40fa-81f1-1782a47f8534)

## Developer Info

* developed and tested using ```python 3.9``` and ```3.10```
* create a virtual environment using `requirements.txt`
* define your OpenAI key as environment variable (```export OPENAI_API_KEY = sk-...```) or create a ```.env``` file (Visual Studio Code) (```OPENAI_API_KEY = sk-...```)

* code is in the `shield` folder
* see [tests](tests) for usage example

## Build

To build and test you additionally need the dependencies in `requirements-dev.txt`

```bash
python setup.py sdist bdist_wheel
```

### Installing build locally

```pip install .```

```python -m spacy download en_core_web_lg```


## Installation and updating
```Distribution model TBD```

Download the pre-built package or build as above.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install SemanticShield like below. 
```bash
TODO
pip install git+https://github.com/semanticbraincorp/SemanticShield
```

## Hosting

For a hosted version (REST API) see [HOSTED.md](HOSTED.md)


## Configuration

Semantic Shield can be configured using Python dictionaries, YAML or JSON strings or files

See [tests](tests) for usage example

Constructors:

> Python dict ShieldConfig.from_dict()

> JSON string ShieldConfig.from_string()

> JSON file ShieldConfig.from_file()

> YAML string ShieldConfig.from_yaml()

> YAML file ShieldConfig.from_yaml_file()



## Usage

### Inline

Validate prompts before sending them to the LLM.

See [tests](tests) for inline usage example

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

### Wrapper

Automatically validate all LLM interactions

```python
with openai_wrapper.semantic_shield():
    try:
        response = do_chat("What is the capital of france?")
        print(response)
    except ShieldException as ex:
        print(ex.result.message)
```

Simple LangChain example

```python
llm = OpenAI()
chat_model = ChatOpenAI()

with openai_wrapper.semantic_shield():
    try:
        text = "You are an idiot"
        result = chat_model.predict(text)
        print(result)

    except ShieldException as ex:
        print(ex.result.message)
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

For a list of supported entity types see [ENTITIES.md](ENTITIES.md)

Text can be sanitized using the following operations:

- tokenize = replace with token
- maks = replace with inauthentic data with the same structure
- redact = remove PII, replace with fixed string (default '_'). Redaction is irreversible.


<b>sanitized with mask (inauthentic data with the same structure)</b>
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

<b>sanitized with tokens</b>
```python
config = ShieldConfig.from_dict(({"pii": {"operation": "tokenize", "permissive": False}}))
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


<b>sanitized by redaction (irreversible)</b>
```python
config = ShieldConfig.from_dict(({"pii": {"operation": "redact", "permissive": False}}))
shield = SemanticShield(config)
result = shield.sanitize(text)
print(result.sanitized)
```

```
My name is _ and my phone number is _.
My social security number is _.
I pay my amex _.
Send payments to acct no _ at TD Bank.
As my name is _, I travel the world running from _.
```
