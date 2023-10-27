import json
import yaml
from yaml.resolver import Resolver

from dataclasses import dataclass, field
from typing import Dict, List

from SemanticShield.config_defaults import ConfigDefaults
from SemanticShield.prompts import Prompts

#TODO - add address regognizer - e.g. https://huggingface.co/spaces/omri374/presidio/blob/main/transformers_recognizer.py

# remove yaml resolver entries for On/Off
for ch in "Oo":
    if len(Resolver.yaml_implicit_resolvers[ch]) == 1:
        del Resolver.yaml_implicit_resolvers[ch]
    else:
        Resolver.yaml_implicit_resolvers[ch] = [x for x in
                Resolver.yaml_implicit_resolvers[ch] if x[0] != 'tag:yaml.org,2002:bool']

@dataclass
class PIIConfig:
    on: bool = ConfigDefaults.pii['on']
    use_placeholders: bool = ConfigDefaults.pii['use_placeholders']
    permissive: bool = ConfigDefaults.pii['permissive']
    permissive_allow: List[str] = field(default_factory=lambda: ConfigDefaults.pii['permissive_allow'])
    max_threshold: float = ConfigDefaults.pii['max_threshold']
    total_threshold: float = ConfigDefaults.pii['total_threshold']
    error: str = ConfigDefaults.pii['error']

@dataclass
class ShieldConfig:

    def __new__(cls):
        self = super().__new__(cls)
        self.pii = PIIConfig(**ConfigDefaults.pii)
        self.jailbreak_prompt = Prompts.jailbreak_prompt
        self.output_moderation_prompt = Prompts.output_moderation_prompt
        self.topics = ConfigDefaults.topics
        self.topic_samples = ConfigDefaults.topic_samples
        self.topic_errors = ConfigDefaults.topic_errors
        self.topic_default_error = ConfigDefaults.topic_default_error

        return self
        
    def __repr__(self):
        return json.dumps(vars(self), sort_keys=True,indent=4, separators=(',', ': ')) 
    
    @classmethod
    def from_dict(cls, obj):
        self = cls()
        self.pii = PIIConfig(**obj.get('pii', ConfigDefaults.pii))
        self.jailbreak_prompt = obj.get('jailbreak_prompt', Prompts.jailbreak_prompt)
        self.output_moderation_prompt = obj.get('output_moderation_prompt', Prompts.output_moderation_prompt)
        self.topics = obj.get('topics', ConfigDefaults.topics)
        self.topic_samples = obj.get('topics', ConfigDefaults.topic_samples)
        self.topic_errors = obj.get('topic_errors', ConfigDefaults.topic_errors)
        self.topic_default_error = obj.get('topic_default_error', ConfigDefaults.topic_default_error)

        return self

    @classmethod
    def from_string(cls, string: str) -> "ShieldConfig":
        obj = json.loads(string)
        return cls.from_dict(obj)

    @classmethod
    def from_file(cls, file_path: str) -> "ShieldConfig":
        with open(file_path, "r") as f:
            text = f.read()
        return cls.from_string(text)

    @classmethod
    def from_yaml(cls, string: str) -> "ShieldConfig":
        obj = yaml.safe_load(string)
        return cls.from_dict(obj)

    @classmethod
    def from_yaml_file(cls, file_path: str) -> "ShieldConfig":
        with open(file_path, "r") as f:
            obj = yaml.safe_load(f)
        return cls.from_dict(obj)
