import json

from device_controller.utility.storage.definitions import DataModel


def decode_response(response):
    return response.decode('utf-8')


def create_table_message(service_name, model_instance: DataModel):
    """
    Creates a message to be sent to the storage service used to define tables
    for modelled data.

    :param service_name:
    :param model_instance:
    :return:
    """
    message = {
        "owner": service_name,
        "table_name": model_instance.__class__.__name__,
        "fields": {}
    }

    fields = model_instance.get_model_fields()
    #print("Fields are: {}".format(fields))

    for name, field in fields:
        message["fields"].update({name: field.__class__.__name__})

    #print("CAN THIS BE JSON: {}".format(message))

    return json.dumps(message).encode('utf-8')
