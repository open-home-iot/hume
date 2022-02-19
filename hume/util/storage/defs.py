from __future__ import annotations

from abc import abstractmethod


SINGLETON = "singleton"


class Model:
    persistent = False
    key = None

    def __str__(self):
        return f"<{self.__class__.__name__} ({vars(self)}>"

    @classmethod
    @abstractmethod
    def decode(cls, *args, **kwargs) -> Model:
        """Decode Redis string fields into intended data types."""
        pass


class ModelError(Exception):
    pass


def model_error(model_name, custom_message=None):
    """
    Raises a model error for the input model name.

    :raises ModelError
    """
    msg = (f"model {model_name} has not been registered"
           if custom_message is None else custom_message)
    raise ModelError(msg)
