from openai.types import ModerationCreateResponse
from openai.types.chat import ChatCompletion

good_moderation_dict = {
    "id": "modr-8kMLFgxtRfMfGHP4pY5bIc7mITQe9",
    "model": "text-moderation-006",
    "results": [
        {
            "categories": {
                "harassment": False,
                "harassment_threatening": False,
                "hate": False,
                "hate_threatening": False,
                "self_harm": False,
                "self_harm_instructions": False,
                "self_harm_intent": False,
                "sexual": False,
                "sexual_minors": False,
                "violence": False,
                "violence_graphic": False,
                "self-harm": False,
                "sexual/minors": False,
                "hate/threatening": False,
                "violence/graphic": False,
                "self-harm/intent": False,
                "self-harm/instructions": False,
                "harassment/threatening": False,
            },
            "category_scores": {
                "harassment": 3.1534711979475105e-06,
                "harassment_threatening": 3.385432600921945e-09,
                "hate": 7.85966491889667e-09,
                "hate_threatening": 3.830443178354931e-13,
                "self_harm": 6.442630717112818e-13,
                "self_harm_instructions": 3.677696778299662e-14,
                "self_harm_intent": 8.662998233703427e-16,
                "sexual": 1.7203082336436637e-07,
                "sexual_minors": 7.996320272596336e-11,
                "violence": 1.5480993170058355e-05,
                "violence_graphic": 1.6704094107922174e-08,
                "self-harm": 6.442630717112818e-13,
                "sexual/minors": 7.996320272596336e-11,
                "hate/threatening": 3.830443178354931e-13,
                "violence/graphic": 1.6704094107922174e-08,
                "self-harm/intent": 8.662998233703427e-16,
                "self-harm/instructions": 3.677696778299662e-14,
                "harassment/threatening": 3.385432600921945e-09,
            },
            "flagged": False,
        }
    ],
}
harassment_moderation_dict = {
    "id": "modr-8kMLFgxtRfMfGHP4pY5bIc7mITQe9",
    "model": "text-moderation-006",
    "results": [
        {
            "categories": {
                "harassment": True,
                "harassment_threatening": False,
                "hate": False,
                "hate_threatening": False,
                "self_harm": False,
                "self_harm_instructions": False,
                "self_harm_intent": False,
                "sexual": False,
                "sexual_minors": False,
                "violence": False,
                "violence_graphic": False,
                "self-harm": False,
                "sexual/minors": False,
                "hate/threatening": False,
                "violence/graphic": False,
                "self-harm/intent": False,
                "self-harm/instructions": False,
                "harassment/threatening": False,
            },
            "category_scores": {
                "harassment": 1.15,
                "harassment_threatening": 3.385432600921945e-09,
                "hate": 7.85966491889667e-09,
                "hate_threatening": 3.830443178354931e-13,
                "self_harm": 6.442630717112818e-13,
                "self_harm_instructions": 3.677696778299662e-14,
                "self_harm_intent": 8.662998233703427e-16,
                "sexual": 1.7203082336436637e-07,
                "sexual_minors": 7.996320272596336e-11,
                "violence": 1.5480993170058355e-05,
                "violence_graphic": 1.6704094107922174e-08,
                "self-harm": 6.442630717112818e-13,
                "sexual/minors": 7.996320272596336e-11,
                "hate/threatening": 3.830443178354931e-13,
                "violence/graphic": 1.6704094107922174e-08,
                "self-harm/intent": 8.662998233703427e-16,
                "self-harm/instructions": 3.677696778299662e-14,
                "harassment/threatening": 3.385432600921945e-09,
            },
            "flagged": True,
        }
    ],
}

good_opeai_dict_55 = {
    "id": "chatcmpl-8kMS1YdAqaUFlc9fuOBjjx85ItE4b",
    "choices": [
        {
            "finish_reason": "stop",
            "index": 0,
            "logprobs": None,
            "message": {
                "content": "no",
                "role": "assistant",
                "function_call": None,
                "tool_calls": None,
            },
        }
    ],
    "created": 1706060081,
    "model": "gpt-3.5-turbo-0613",
    "object": "chat.completion",
    "system_fingerprint": None,
    "usage": {"completion_tokens": 10, "prompt_tokens": 45, "total_tokens": 55},
}
bad_opeai_dict_55 = {
    "id": "chatcmpl-8kMS1YdAqaUFlc9fuOBjjx85ItE4b",
    "choices": [
        {
            "finish_reason": "stop",
            "index": 0,
            "logprobs": None,
            "message": {
                "content": "yes",
                "role": "assistant",
                "function_call": None,
                "tool_calls": None,
            },
        }
    ],
    "created": 1706060081,
    "model": "gpt-3.5-turbo-0613",
    "object": "chat.completion",
    "system_fingerprint": None,
    "usage": {"completion_tokens": 10, "prompt_tokens": 45, "total_tokens": 55},
}


good_moderation = ModerationCreateResponse(**good_moderation_dict) 
harassment_moderation = ModerationCreateResponse(**harassment_moderation_dict)

good_opeai_55 = ChatCompletion(**good_opeai_dict_55)
bad_opeai_55 = ChatCompletion(**bad_opeai_dict_55)
politics_opeai_55 = ChatCompletion(**bad_opeai_dict_55)