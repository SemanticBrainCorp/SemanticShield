
import logging
import os
from typing import Callable, Dict, Optional

import spacy

from openai_funcs import moderate_prompt, run_prompt
from shield.moderation_exception import ModerationException
from shield.shield_result import ShieldResult
from shield.llm_result import LLMCheckResult

from shield.pii import PIIAnalyzer

from shield.prompts import Prompts
from shield.shield_config import ShieldConfig

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -15s %(filename) -15s %(funcName) '
              '-15s %(lineno) -5d: %(message)s')

logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("faker").setLevel(logging.WARNING)
logging.getLogger("presidio-analyzer").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


try:
    nlp = spacy.load("en_core_web_lg")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_lg")
    nlp = spacy.load("en_core_web_lg")

class SemanticShield:
    def __init__(
        self,
        config: Optional[ShieldConfig] = ShieldConfig(),
    ):
        self.config = config
        self.pii_analyzer = PIIAnalyzer(config.pii)

    def check_jailbreak(self, prompt: str, moderate: bool = True)->ShieldResult:
        #checks for jailbreaking attempts
        prompt = self.config.jailbreak_prompt.replace('##PROMPT##', prompt)
        llm_check_result = run_prompt(prompt, moderate=moderate)
        return ShieldResult(llm_check_result.fail, "I am not able to answer the question.", usage = llm_check_result.usage)

    def check_output(self, response: str, moderate: bool = True)->LLMCheckResult:
        #checks for undesireable outputs
        prompt = self.output_moderation_prompt.replace('##RESPONSE##', response)
        llm_check_result = run_prompt(prompt, moderate=moderate)
        return llm_check_result

    def check_prompt_moderation(self, prompt: str, _=True)->ShieldResult:
        #run openai prompt moderation
        #ignore moderation parameter, there for signature consistency
        try:
            moderate_prompt(prompt)
        except ModerationException as ex:

            return ShieldResult(True, f'Your request has been flagged by SemanticShield moderation: {", ".join(ex.flags)}')
        return ShieldResult(False, None)

    def check_topic(self, input: str, topic: str, moderate: bool = True)->ShieldResult:
        #verify prohibited topics (by example or by allowing chatgpt to classify input)
        if topic in self.config.topic_samples:
            prompt = Prompts.topics_prompt.replace('##EXAMPLES', self.config.topic_samples[topic])
        else:
            prompt = Prompts.topics_default_prompt
        prompt = prompt.replace('##TOPIC##', topic)
        prompt = prompt.replace('##INPUT##', input)
        
        result = run_prompt(prompt, moderate=moderate)
        if result.fail:
            if topic in self.config.topic_errors:
                message = self.config.topic_errors[topic]
            else:
                message = self.config.topic_default_error
        else:
            message = "Success"
        return ShieldResult(result.fail, message, usage=result.usage)
    
    def check_topics(self, input: str, moderate: bool = True)->ShieldResult:
        #check for prohibited topics
        for topic in self.config.topics:
            result = self.check_topic(input, topic, moderate)
            if result.fail:
                return result
        return ShieldResult(False, None, usage=result.usage)
    
    def check_pii_score(self, text: str) -> (float, float):
        max_score, total_score = self.pii_analyzer.score(text)
        return max_score, total_score
    
    def check_pii(self, text: str, usage_total: int = 0) ->ShieldResult:
        pii_max, pii_total = self.check_pii_score(text)
        if self.config.pii.on:
            if pii_max>self.config.pii.max_threshold or pii_total>self.config.pii.total_threshold:
                return ShieldResult(True, 'PII present in text', pii_max=pii_max, pii_total=pii_total, usage=usage_total)
        return ShieldResult(False, None, pii_max=pii_max, pii_total=pii_total, usage=usage_total)
    

    def do_check(self, text: str, usage_total, checker_func: Callable[[str], tuple[float, float]], moderate=True) -> (bool, ShieldResult, float):
        failed = False
        result = None
        check_result = checker_func(text, moderate)
        usage_total += check_result.usage
        if check_result.fail:
            failed = True
            result = ShieldResult(True, check_result.message, usage=usage_total)
        return failed, result, usage_total
    
    def __call__(self, text: str)->ShieldResult:

        if not isinstance(text, str):
            logging.error(f'Invalid Input Type - {type(text)}')
            raise TypeError('Incompatible argument, must be string')

        failed = False
        usage_total = 0
        result = self.check_pii(text, usage_total=usage_total)
        if result.fail:
            failed = True
        pii_max = result.pii_max
        pii_total = result.pii_total
        if not failed:
            failed, result, usage_total = self.do_check(text, usage_total, self.check_prompt_moderation)
        if not failed:
            failed, result, usage_total = self.do_check(text, usage_total, self.check_jailbreak, moderate=False)
        if not failed:
            failed, result, usage_total = self.do_check(text, usage_total, self.check_topics, moderate=False)
        if not failed:
            result = ShieldResult(False, '', usage=usage_total)
        result.pii_max = pii_max
        result.pii_total = pii_total

        return result

    def sanitize(self, text: str):
        if not isinstance(text, str):
            logging.error(f'Invalid Input Type - {type(text)}')
            raise TypeError('Incompatible argument, must be string')

        text, replacement_map = self.pii_analyzer.pseudo(text=text)
        return ShieldResult(False if len(replacement_map) == 0 else True, '', sanitized=text, replacement_map=replacement_map )

    def revert(self, text: str, replacement_map: dict)->str:
        if not isinstance(text, str):
            logging.error(f'Invalid Input Type - {type(text)}')
            raise TypeError('Incompatible argument, must be string')
        text = self.pii_analyzer.revert( text, replacement_map)
        return text
