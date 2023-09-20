import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Type
from pprint import pprint

from shield.config_defaults import ConfigDefaults
from shield.prompts import Prompts

#TODO - add address regognizer - e.g. https://huggingface.co/spaces/omri374/presidio/blob/main/transformers_recognizer.py

@dataclass
class PIIConfig:
    on: bool = ConfigDefaults.pii['on']
    use_placeholders: bool = ConfigDefaults.pii['use_placeholders']
    permissive: bool = ConfigDefaults.pii['permissive']
    permissive_allow: List[str] = field(default_factory=lambda: ConfigDefaults.pii['permissive_allow'])
    max_threshold: float = ConfigDefaults.pii['max_threshold']
    total_threshold: float = ConfigDefaults.pii['total_threshold']

@dataclass
class ShieldConfig:
    pii: PIIConfig = PIIConfig(**ConfigDefaults.pii)
    jailbreak_prompt: str = Prompts.jailbreak_prompt
    output_moderation_prompt: str = Prompts.output_moderation_prompt
    topics: List[str] = field(default_factory=lambda: ConfigDefaults.topics)
    topic_samples: Dict[str, str] = field(default_factory=lambda: ConfigDefaults.topic_samples)
    topic_errors: Dict[str, str] = field(default_factory=lambda: ConfigDefaults.topic_errors)
    topic_default_error: str = ConfigDefaults.topic_default_error


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
        return ShieldConfig.from_dict(obj)

    @classmethod
    def from_file(cls, file_path: str) -> "ShieldConfig":
        with open(file_path, "r") as f:
            text = f.read()
        return cls.from_string(text)
