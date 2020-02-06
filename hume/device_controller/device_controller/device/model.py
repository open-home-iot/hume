from device_controller.utility.storage.definitions import DataModel, PRIMARY_KEY


class Device(DataModel):

    device_id = int(PRIMARY_KEY)

    def local(self):
        pass

    def persistent(self):
        return self.device_id,
