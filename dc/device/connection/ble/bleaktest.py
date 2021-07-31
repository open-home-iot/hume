import asyncio

import bleak
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


async def run():
    devices = await BleakScanner.discover()
    device = None
    for d in devices:
        print(f"{d.address}: {d.name}")

        if d.name == "Feather nRF52832":
            device = d

    client = bleak.BleakClient(device.address)
    await client.connect()

    await asyncio.sleep(3)

    await client.disconnect()

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
