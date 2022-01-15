import abc


class App(abc.ABC):

    @abc.abstractmethod
    def pre_start(self):
        """Called before start"""
        ...

    @abc.abstractmethod
    def start(self):
        """Called before post_start"""
        ...

    @abc.abstractmethod
    def post_start(self):
        """Called after start"""
        ...

    @abc.abstractmethod
    def pre_stop(self):
        """Called before stop"""
        ...

    @abc.abstractmethod
    def stop(self):
        """Called before post_stop"""
        ...

    @abc.abstractmethod
    def post_stop(self):
        """Called after stop"""
        ...
