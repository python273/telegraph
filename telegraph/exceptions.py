class TelegraphException(Exception):
    """Base exception class for all Telegraph-related errors."""

    pass


class ParsingException(Exception):
    """Base exception class for all parsing-related errors."""

    pass


class NotAllowedTag(ParsingException):
    """Raised when an HTML tag is not supported by the parser."""

    pass


class InvalidHTML(ParsingException):
    """Raised when the provided HTML is malformed or invalid."""

    pass


class RetryAfterError(TelegraphException):
    """Raised when flood control is triggered and retry is required after a delay.

    Attributes:
        retry_after (int): Time in seconds after which the request can be retried.
    """

    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f"Flood control exceeded. Retry in {retry_after} seconds")
