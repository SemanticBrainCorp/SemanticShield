class ConfigDefaults(object):

    pii = {
        "on": True,
        "permissive": False,
        "use_placeholders": False,
        "max_threshold": 0.5,
        "total_threshold": 2.0,
        "permissive_allow": ["PERSON", "DATE_TIME", "NRP"]
    }
    topics = [
        'political'
    ]

    topic_samples = {
        'political' : """
            'what are your political beliefs?',
            'what are Trump's chances of being elected president again?',
            'thoughts on the president?',
            'left wing',
            'right wing',
            'What do you think about the government?',
            'Which party should I vote for?',
        """,
    }

    topic_errors = {
        'political' : "I don't like to talk about politics"
    }
    topic_default_error = "Thank you for sharing your thoughts. I'm here to help if you have any questions or concerns. Let's work together to find a solution."
