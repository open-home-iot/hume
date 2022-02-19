from __future__ import annotations

from util.storage import Model, SINGLETON


class HumeUser(Model):
    persistent = True
    key = SINGLETON

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    @classmethod
    def decode(cls, username: str = None, password: str = None) -> HumeUser:
        return cls(username, password)


class BrokerCredentials(Model):
    persistent = True
    key = SINGLETON

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    @classmethod
    def decode(cls, username: str = None, password: str = None) -> \
            BrokerCredentials:
        return cls(username, password)


class HintAuthentication(Model):
    key = SINGLETON

    def __init__(self, session_id, csrf_token=None):
        self.session_id = session_id
        self.csrf_token = csrf_token

    @classmethod
    def decode(cls, *args, **kwargs):
        pass
