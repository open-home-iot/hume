from abc import ABC, abstractmethod

NO_TIER_DEFINED = "NONE"


class Dispatch(ABC):
    """
    Abstract class used as an interface for services that want to provide their
    service to other services.
    """
    dispatch_tier = NO_TIER_DEFINED

    @property
    @abstractmethod
    def dispatch_id(self) -> str:
        """Uniquely identifies a service for dispatch."""
        ...

    @abstractmethod
    def on_dispatch(self, message):
        """Called when dispatching a message from another service."""
        ...

    @abstractmethod
    def set_dispatch_tier(self, dispatch_tier: str) -> str:
        """
        Setter for dispatch_tier as this is not determined by the service
        itself, but provided by the administrating application.
        """
        ...

    def get_dispatch_address(self) -> tuple:
        """
        Getter for the fully qualified dispatch address.

        :return: tuple with (tier, dispatch id)
        """
        return self.dispatch_tier, self.dispatch_id


_dispatch_registry = dict()


def register(tier, service):
    """
    Registers the parameter service as a dispatch provider.

    Registering service must implement the dispatch interface.

    :param str tier:
    :param class service:
    """
    assert issubclass(service.__class__, Dispatch)

    service.set_dispatch_tier(tier)

    print("Initial dispatch registry:")
    print(_dispatch_registry)

    tier_dict = _dispatch_registry.get(tier)
    tier_update = {service.dispatch_id: service}

    # Nothing exists for this tier yet
    if tier_dict is None:
        # Set brand new tier info
        print("Tier was empty, setting: {}".format(tier_update))

        _dispatch_registry.update({tier: tier_update})
    else:
        # Update what is already in the tier
        tier_dict.update(tier_update)

    print("Updated dispatch registry:")
    print(_dispatch_registry)


def dispatch(to, message):
    """
    Dispatches the parameter message to the to parameter dispatch service.

    :param tuple to:
    :param message:
    """
    print("dispatching to: {} message: {}".format(to, message))
    (tier, dispatch_id) = to

    tier_dict = _dispatch_registry.get(tier)
    tier_dict.get(dispatch_id).on_dispatch(message)
