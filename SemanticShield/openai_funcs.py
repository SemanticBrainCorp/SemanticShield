import logging
import openai
import os
from SemanticShield.errors import APIKEYException, ModerationException
from SemanticShield.llm_result import LLMCheckResult

from SemanticShield.openai_model import OpenAIModel
from SemanticShield.openai_settings import OpenAISettings

ENGINE=OpenAISettings.ENGINE
CHAT_ENGINE=OpenAISettings.CHAT_ENGINE
MODEL = OpenAIModel.CHAT_GPT

initialized = False
def init_openai_key():
    global initialized
    if not initialized:
        if 'OPENAI_API_KEY' not in os.environ:
            raise APIKEYException(f"OPENAI key not set")
        openai.api_key = os.environ['OPENAI_API_KEY']
        initialized = True

def moderate_prompt(prompt: str):
    init_openai_key()
    #run the prompt against OpenAIs moderation API
    response = openai.Moderation.create(
        input=prompt
    )
    output = response["results"][0]
    if output['flagged']:
        flags = [i for i in output['categories'] if output['categories'][i]]

        # TODO - report error
        raise ModerationException(flags=flags)

def standardize_result(result: str) -> bool:
    #convert llm response to pass/fail
    result = result.lower().replace('.','')
    return result == 'yes'

def run_prompt(prompt: str, max_tokens: int = 100, temperature: float = 0.7, chat: bool =True, moderate: bool = True, backup_create=None, backup_chat_create=None) -> LLMCheckResult:
    init_openai_key()
    #run a validation prompt, respond with pass/fail and token usage
    if moderate:
        try:
            moderate_prompt(prompt)
        except openai.error.Timeout:
            logging.exception("OpenAI API request timed out")
            raise
    
    if MODEL == OpenAIModel.CHAT_GPT and chat is True:
        func = openai.ChatCompletion.create
        if backup_chat_create:
            func = backup_chat_create
        response = func(
            model=CHAT_ENGINE,
            temperature=temperature,
            messages=[{
                "role": "user",
                "content": prompt
            }])
        usage = response['usage']['total_tokens']
        result = response['choices'][0]['message']['content']
    else:
        func = openai.Completion.create
        if backup_create:
            func = backup_create
        response = func(
            engine=ENGINE,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        usage = response['usage']['total_tokens']
        result = response['choices'][0]['text']
    return LLMCheckResult(standardize_result(result), usage)

