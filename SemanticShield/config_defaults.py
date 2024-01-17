from SemanticShield.yaml_parser import yaml_file_parser

sensitive_def = {
    'on': True,
    'policy': {
        'min_length': 8,
        'num_uppercase': 1,
        'num_lowercase': 1,
        'num_numerics': 1,
        'num_symbols': 1
    },
    'error': 'Please rephrase without using sensitive information.'
}

class ConfigDefaults(object):

    obj = yaml_file_parser('config_defaults.yml')

    if 'pii' in obj:
        pii = obj['pii']
    else:
        pii = None
    if 'sensitive' in obj:
        sensitive = obj['sensitive']
    else:
        sensitive = sensitive_def
    if 'profanity' in obj:
        profanity = obj['profanity']
    else:
        profanity = 'imprecise'
    if 'topics' in obj:
        topics = obj['topics']
    else:
        topics = None
    if 'topic_samples' in obj:
        topic_samples = obj['topic_samples']
    else:
        topic_samples = None
    if 'topic_errors' in obj:
        topic_errors = obj['topic_errors']
    else:
        topic_errors = None
    if 'topic_default_error' in obj:
        topic_default_error = obj['topic_default_error']
    else:
        topic_default_error = None
