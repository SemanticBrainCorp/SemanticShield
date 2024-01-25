import logging


from SemanticShield.client import get_openai_client, get_moderation_client
from SemanticShield.errors import APIKEYException, ModerationException
from SemanticShield.llm_result import LLMCheckResult

from SemanticShield.openai_settings import OpenAISettings

ENGINE=OpenAISettings.ENGINE
CHAT_ENGINE=OpenAISettings.CHAT_ENGINE

initialized = False
def init_openai_key():
    global initialized, client, moderation_client
    if not initialized:
        client = get_openai_client()
        moderation_client = get_moderation_client()
        initialized = True

def moderate_prompt(prompt: str):
    init_openai_key()
    #run the prompt against OpenAIs moderation API
    response = moderation_client.moderations.create(input=prompt)
    print(response)
    output = response.results[0]
    if output.flagged:
        flags = [f for f in output.categories.model_fields_set if getattr(output.categories, f)]        
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
        except Exception:
            logging.exception("OpenAI API request timed out")
            raise
    
    func = client.chat.completions.create
    if backup_chat_create:
        func = backup_chat_create
    response = func(
        model=CHAT_ENGINE,
        temperature=temperature,
        messages=[{
            "role": "user",
            "content": prompt
        }])
    usage = response.usage.total_tokens
    result = response.choices[0].message.content.strip()
    return LLMCheckResult(standardize_result(result), usage)
