from contextlib import contextmanager
import functools
import logging

import openai
from SemanticShield import SemanticShield, ShieldConfig, ShieldException

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -15s %(filename) -15s %(funcName) '
              '-15s %(lineno) -5d: %(message)s')
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
#logging.getLogger("requests").setLevel(logging.WARNING)

backup_create = openai.Completion.create
backup_chat_create = openai.ChatCompletion.create


def extract_query(messages):
    user_prompt = [
        message["content"] for message in messages if message["role"] == "user"
    ][0]
    return user_prompt

    
def ss_openai_wrapper(func, shield):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        messages = kwargs.get("messages")

        if messages:
            query = extract_query(messages)

            result = shield(query)
            if result.fail:
                raise ShieldException(result)

        response = func(*args, **kwargs)
        if messages:
            user_prompt = [message["content"] for message in messages if message["role"] == "user"][0]
            system_prompt_list = [message["content"] for message in messages if message["role"] == "system"]
            system_prompt = system_prompt_list[0] if len(system_prompt_list) > 0 else ''
            llm_response = ""
            if func.__name__ == "create":
                if "ChatCompletion" in func.__qualname__:
                    llm_response = response["choices"][0]["message"]["content"].strip()
                elif "Completion" in func.__qualname__:
                    llm_response = response.choices[0].text.strip()

            # TODO custom logger
            logging.info(
                {
                    "prompt": user_prompt,
                    "system_prompt": system_prompt,
                    "response": llm_response,
                }
            )
        return response
    return wrapper

def init_shield(configuration, backup_create, backup_chat_create):
    if configuration is None:
        config = ShieldConfig.from_yaml_file('config_defaults.yml')
    else:
        config = ShieldConfig.from_dict(configuration)
    shield = SemanticShield(config, backup_chat_create=backup_chat_create, backup_create=backup_create)
    return shield

@contextmanager
def semantic_shield(configuration=None):
    global backup_create
    global backup_chat_create
    
    shield = init_shield(configuration, backup_create, backup_chat_create)
    openai.Completion.create = ss_openai_wrapper(backup_create, shield)
    openai.ChatCompletion.create = ss_openai_wrapper(backup_chat_create, shield)
    try:
        yield
    finally:
        openai.Completion.create = backup_create
        openai.ChatCompletion.create = backup_chat_create
