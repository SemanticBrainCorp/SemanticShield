from unittest.mock import Mock, patch

class MockOpenAIChatCompletion:
    def __init__(
        self,
        model=None,
        encoding_name=None,
        max_tokens=None,
        api_key=None,
        api_base=None,
    ):
        # mock class
        pass

class MockOpenAIModeration:
    def __init__(
        self,
        model=None,
        encoding_name=None,
        max_tokens=None,
        api_key=None,
        api_base=None,
    ):
        # mock class
        pass


class MockResponse:
    def __init__(self, data=None):
        self.data = data or []

    def json(self):
        return self.data
