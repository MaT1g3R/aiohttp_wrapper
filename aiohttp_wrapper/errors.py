class HTTPStatusError(Exception):
    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg

    def __str__(self):
        return 'HTTPStatusError:\nCode: {}\nMessage: {}'.format(
            self.code, self.msg
        )

    def __repr__(self):
        return 'HTTPStatusError({}, {})'.format(self.code, self.msg)
