import os
from openai import OpenAI

from SemanticShield.errors import APIKEYException

def get_openai_client():
    if 'LOCAL_BASE_URL' not in os.environ:
        if 'OPENAI_API_KEY' not in os.environ:
            raise APIKEYException(f"OPENAI key not set")        
        client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    else:
        client = OpenAI(base_url=os.environ['LOCAL_BASE_URL'], api_key="not-needed")
    return client

def get_moderation_client():
    if 'OPENAI_API_KEY' not in os.environ:
        raise APIKEYException(f"OPENAI key not set")        
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    return client
