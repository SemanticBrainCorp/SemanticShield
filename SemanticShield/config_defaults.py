from SemanticShield.yaml_parser import yaml_file_parser

class ConfigDefaults(object):

    obj = yaml_file_parser('config_defaults.yml')

    if 'pii' in obj:
        pii = obj['pii']
    else:
        pii = None
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

    # pii = {
    #     "on": True,
    #     "permissive": False,
    #     "use_placeholders": False,
    #     "max_threshold": 0.5,
    #     "total_threshold": 2.0,
    #     "permissive_allow": ["PERSON", "DATE_TIME", "NRP"],
    #     "error": "Please rephrase without using personal and confidential information."
    # }
    # topics = [
    #     'political'
    # ]

    # topic_samples = {
    #     'political' : """
    #         'what are your political beliefs?',
    #         'what are Trump's chances of being elected president again?',
    #         'thoughts on the president?',
    #         'left wing',
    #         'right wing',
    #         'What do you think about the government?',
    #         'Which party should I vote for?',
    #     """,
    # }

    # topic_errors = {
    #     'political' : "I don't like to talk about politics"
    # }
    # topic_default_error = "Thank you for sharing your thoughts. I'm here to help if you have any questions or concerns. Let's work together to find a solution."
