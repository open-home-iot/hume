DEVICE_UUID_LED = "824df4c1-961c-423e-81ea-5e1289da77cf"
DEVICE_UUID_AQUARIUM = "824df4c2-961c-423e-81ea-5e1289da77cf"

DEVICE_UUIDS = [DEVICE_UUID_LED, DEVICE_UUID_AQUARIUM]

BASIC_LED_CAPS = {
    'uuid': DEVICE_UUID_LED,
    'name': 'Basic Lamp',
    'category': 1,
    'type': 1,
    'states': [
        {
            'id': 0,
            'control': [{'on': 1}, {'off': 0}]
        }
    ]
}

AQUARIUM_CAPS = {
    'uuid': DEVICE_UUID_AQUARIUM,
    'name': 'Aquarium',
    'category': 2,
    'type': 666,
    'states': [
        {
            'id': 0,
            'lighting': [{'on': 1}, {'off': 0}]
        },
        {
            'id': 1,
            'pump': [{'high': 2}, {'medium': 1}, {'low': 0}]
        }
    ]
}
