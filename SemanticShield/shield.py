
import logging
from typing import Callable, Dict, Optional

# import os
# import spacy

from SemanticShield.openai_funcs import moderate_prompt, run_prompt
from SemanticShield.errors import ModerationException
from SemanticShield.shield_result import ShieldResult
from SemanticShield.llm_result import LLMCheckResult

from SemanticShield.pii_analyzer import PIIAnalyzer

from SemanticShield.prompts import Prompts
from SemanticShield.shield_config import ShieldConfig

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -15s %(filename) -15s %(funcName) '
              '-15s %(lineno) -5d: %(message)s')

logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("faker").setLevel(logging.WARNING)
logging.getLogger("presidio-analyzer").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# model = "en_core_web_lg"
# try:
#     nlp = spacy.load(model)
# except OSError:
#     import spacy.cli
#     spacy.cli.download(model)
#     nlp = spacy.load(model)

class SemanticShield:
    def __init__(
        self,
        config: Optional[ShieldConfig] = ShieldConfig(),
        backup_create: Optional[any] = None,
        backup_chat_create: Optional[any] = None
    ):
        self.config = config
        self.pii_analyzer = PIIAnalyzer(config.pii)
        self.backup_create = backup_create
        self.backup_chat_create = backup_chat_create

    def check_jailbreak(self, prompt: str, moderate: bool = True)->ShieldResult:
        #checks for jailbreaking attempts
        prompt = self.config.jailbreak_prompt.replace('##PROMPT##', prompt)
        llm_check_result = run_prompt(prompt, moderate=moderate, backup_create=self.backup_create, backup_chat_create=self.backup_chat_create)
        return ShieldResult(llm_check_result.fail, fail_type='JAILBREAK', message="I am not able to answer the question.", usage = llm_check_result.usage)

    def check_output(self, response: str, moderate: bool = True)->LLMCheckResult:
        #checks for undesireable outputs
        prompt = self.output_moderation_prompt.replace('##RESPONSE##', response)
        llm_check_result = run_prompt(prompt, moderate=moderate, backup_create=self.backup_create, backup_chat_create=self.backup_chat_create)
        return llm_check_result

    def check_prompt_moderation(self, prompt: str, _=True)->ShieldResult:
        #run openai prompt moderation
        #ignore moderation parameter, there for signature consistency
        try:
            moderate_prompt(prompt)
        except ModerationException as ex:
            return ShieldResult(
                True,
                message = f'Your request has been flagged by SemanticShield moderation: {", ".join(ex.flags)}',
                fail_type = 'MODERATION',
                fail_data = ex.flags
            )
        return ShieldResult(False)

    def check_topic(self, input: str, topic: str, moderate: bool = True)->ShieldResult:
        #verify prohibited topics (by example or by allowing chatgpt to classify input)
        if topic in self.config.topic_samples:
            prompt = Prompts.topics_prompt.replace('##EXAMPLES', self.config.topic_samples[topic])
        else:
            prompt = Prompts.topics_default_prompt
        prompt = prompt.replace('##TOPIC##', topic)
        prompt = prompt.replace('##INPUT##', input)
        
        result = run_prompt(prompt, moderate=moderate, backup_create=self.backup_create, backup_chat_create=self.backup_chat_create)
        if result.fail:
            if topic in self.config.topic_errors:
                message = self.config.topic_errors[topic]
            else:
                message = self.config.topic_default_error
        else:
            message = "Success"
        return ShieldResult(
            result.fail,
            message=message,
            fail_type='TOPIC',
            fail_data=[topic],
            usage=result.usage
        )
    
    def check_topics(self, input: str, moderate: bool = True)->ShieldResult:
        #check for prohibited topics
        for topic in self.config.topics:
            result = self.check_topic(input, topic, moderate)
            if result.fail:
                return result
        return ShieldResult(False, usage=result.usage)
    
    def check_pii_score(self, text: str) -> (float, float):
        max_score, total_score = self.pii_analyzer.score(text)
        return max_score, total_score
    
    def check_pii(self, text: str, usage_total: int = 0) ->ShieldResult:
        pii_max, pii_total = self.check_pii_score(text)
        if self.config.pii.on:
            if pii_max>self.config.pii.max_threshold or pii_total>self.config.pii.total_threshold:
                return ShieldResult(True, fail_type='PII', message=self.config.pii.error, pii_max=pii_max, pii_total=pii_total, usage=usage_total)
        return ShieldResult(False, pii_max=pii_max, pii_total=pii_total, usage=usage_total)
    

    def do_check(self, text: str, usage_total, checker_func: Callable[[str], ShieldResult], moderate=True) -> (bool, ShieldResult, float):
        failed = False
        result = None
        check_result = checker_func(text, moderate)
        usage_total += check_result.usage
        if check_result.fail:
            failed = True
            result = ShieldResult(True, message=check_result.message, fail_type=check_result.fail_type, fail_data=check_result.fail_data, usage=usage_total)
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
            result = ShieldResult(False, usage=usage_total)
        result.pii_max = pii_max
        result.pii_total = pii_total

        return result

    def sanitize(self, text: str):
        if not isinstance(text, str):
            logging.error(f'Invalid Input Type - {type(text)}')
            raise TypeError('Incompatible argument, must be string')

        text, replacement_map = self.pii_analyzer.pseudo(text=text)
        return ShieldResult(
            False if len(replacement_map) == 0 else True,
            fail_type=None if len(replacement_map) == 0 else 'PII',
            sanitized=text,
            replacement_map=replacement_map )

    def revert(self, text: str, replacement_map: dict)->str:
        if not isinstance(text, str):
            logging.error(f'Invalid Input Type - {type(text)}')
            raise TypeError('Incompatible argument, must be string')
        text = self.pii_analyzer.revert( text, replacement_map)
        return text
