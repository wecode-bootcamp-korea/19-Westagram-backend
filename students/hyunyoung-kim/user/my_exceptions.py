class InvalidEmail(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class InvalidPassword(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class AlreadyExistEmail(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class AlreadyExistNickname(Exception):
    def __init__(self, msg):
        super().__init__(msg)