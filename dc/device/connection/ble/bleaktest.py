import asyncio

from bleak import BleakScanner


"""
{
    'address': 'B7D59079-55BC-49CF-9E03-20B595D1421E', 
    'name': 'Feather nRF52832', 
    'details': <CBPeripheral: 0x7fbae8e04550, identifier = B7D59079-55BC-49CF-9E03-20B595D1421E, name = Feather nRF52832, mtu = 0, state = disconnected>, 
    'rssi': -69, 
    'metadata': {
        'uuids': ['6e400001-b5a3-f393-e0a9-e50e24dcca9e'],  <--- UART service identifier
        'manufacturer_data': {},  <--- Put HOME tag to identify this is a HOME-compatible device
        'service_data': {}, 
        'delegate': <CentralManagerDelegate: 0x7fbaea649a10>
    }
}
"""


def cb(wat, device):
    print(wat)
    print(device)
    print(device.__dict__)


async def run():
    devices = await BleakScanner.discover(timeout=5.0)

    device = None
    for d in devices:
        if d.name == "Basic LED":
            device = d
            print(f"\n{d.address}: {d.name}")
            for k, v in d.__dict__.items():
                if isinstance(v, dict):
                    print(f"{k}:")
                    for subk, subv in v.items():
                        print(f"\t{subk}: {subv}")

                    continue

                print(f"{k}: {v}")

    nus_svc = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"

    print("")
    print("> Checking NUS status ...")
    if nus_svc in device.metadata["uuids"]:
        print("> NUS present, proceeding to check for HOME service ID")

    home_svc_data_uuid = "0000a1b2-0000-1000-8000-00805f9b34fb"
    expected_home_svc_val = "1337"
    home_svc_data = device.metadata['service_data'][home_svc_data_uuid].hex()
    if expected_home_svc_val == home_svc_data:
        print("> Yay, HOME SVC value was correct: 1337!")

    # client = bleak.BleakClient(device.address)
    # await client.connect()
    #
    # await asyncio.sleep(3)
    #
    # await client.disconnect()

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
