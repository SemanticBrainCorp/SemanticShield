import http
class ModerationException(http.client.HTTPException):
    """Exception raised when OpenAI flags the prompt.

    Attributes:
        flags -- list of flagged categories
    """
    def __init__(self, flags, description="Moderation error"):
        self.code = 400
        self.flags = flags
        self.description = description
        super().__init__(self.description)

class APIKEYException(Exception):
    """Exception raised when OpenAI key is missing."""
    pass
