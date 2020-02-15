import json

from device_controller.utility.storage.definitions import DataModel, \
    has_relation, is_enum, is_key, ForeignKey


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

    for column, field in fields:
        message["fields"].update({
            column: make_field_string(field)
        })

    #print("CAN THIS BE JSON: {}".format(message))
    print(json.dumps(message, indent=4, sort_keys=True))

    return json.dumps(message).encode('utf-8')


def make_field_string(field):
    field_name = field.__class__.__name__

    if has_relation(field):
        field_relation = field.cls.__name__

        key = ""
        if isinstance(field, ForeignKey) and is_key(field):
            key = ", KEY"

        return f"{field_name}({field_relation}{key})"

    elif is_enum(field):
        field_type = type(field.options[1]).__name__

        return f"{field_name}({field_type})"

    return field_name
