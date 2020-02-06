from abc import ABC, abstractmethod


NO_TIER_DEFINED = "NONE"


class Dispatch(ABC):
    """
    Abstract class used as an interface for services that want to provide their
    service to other services.
    """
    _dispatch_tier = NO_TIER_DEFINED

    @property
    def dispatch_tier(self) -> str:
        return self._dispatch_tier

    @dispatch_tier.setter
    def dispatch_tier(self, dispatch_tier: str):
        """
        Setter for dispatch_tier as this is not determined by the service
        itself, but provided by the administrating application.
        """
        self._dispatch_tier = dispatch_tier

    @property
    @abstractmethod
    def dispatch_id(self) -> str:
        """Uniquely identifies a service for dispatch."""
        ...

    @abstractmethod
    def on_dispatch(self, message):
        """Called when dispatching a message from another service."""
        ...
