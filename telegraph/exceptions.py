

class TelegraphException(Exception):
    pass


class ParsingException(Exception):
    pass


class NotAllowedTag(ParsingException):
    pass


class InvalidHTML(ParsingException):
    pass
