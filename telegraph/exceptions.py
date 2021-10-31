

class TelegraphException(Exception):
    pass


class ParsingException(Exception):
    pass


class NotAllowedTag(ParsingException):
    pass


class InvalidHTML(ParsingException):
    pass


class RetryAfterError(TelegraphException):
    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f'Flood control exceeded. Retry in {retry_after} seconds')
