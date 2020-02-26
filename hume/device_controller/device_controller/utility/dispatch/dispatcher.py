import logging

from device_controller.utility.dispatch import Dispatch


LOGGER = logging.getLogger(__name__)

_dispatch_registry = dict()


def register(tier, service):
    """
    Registers the parameter service as a dispatch provider.

    Registering service must implement the dispatch interface.

    :param str tier: tier to register service with
    :param class service: service to register with dispatch tier
    """
    LOGGER.info(f"Registering {service} to tier {tier}")

    assert issubclass(service.__class__, Dispatch)

    service.dispatch_tier = tier

    tier_dict = _dispatch_registry.get(tier)
    tier_update = {service.dispatch_id: service}

    # Nothing exists for this tier yet
    if tier_dict is None:
        # Set brand new tier info
        _dispatch_registry.update({tier: tier_update})
    else:
        # Update what is already in the tier
        tier_dict.update(tier_update)

    LOGGER.debug(f"new dispatch registry: {_dispatch_registry}")


def dispatch(to, message):
    """
    Dispatches the parameter message to the to parameter dispatch service.

    :param tuple to: recipient
    :param message: message to send
    """
    LOGGER.debug(f"dispatching {message} to {to}")
    (tier, dispatch_id) = to

    tier_dict = _dispatch_registry.get(tier)
    tier_dict.get(dispatch_id).on_dispatch(message)
