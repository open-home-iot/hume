import json

from device_controller.utility.storage.definitions import DataModel


def create_table_message(service_name, model_instance: DataModel):
    """
    Creates a message to be sent to the storage service used to define tables
    for modelled data.

    :param service_name:
    :param model_instance:
    :return:
    """
    message = {
        "owner": service_name
    }

    fields = model_instance.get_model_fields()
    print("Fields are: {}".format(fields))

    return json.dumps(message).encode('utf-8')
