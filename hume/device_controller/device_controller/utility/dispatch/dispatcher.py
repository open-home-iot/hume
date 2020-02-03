from device_controller.utility.dispatch import Dispatch


_dispatch_registry = dict()


def register(tier, service):
    """
    Registers the parameter service as a dispatch provider.

    Registering service must implement the dispatch interface.

    :param str tier:
    :param class service:
    """
    assert issubclass(service.__class__, Dispatch)

    service.dispatch_tier = tier

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
