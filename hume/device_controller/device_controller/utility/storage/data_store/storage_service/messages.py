import json
import logging

from device_controller.utility.storage.definitions import DataModel, \
    has_relation, is_enum, is_key, ForeignKey


LOGGER = logging.getLogger(__name__)


def decode_response(response):
    """
    Decodes a storage service response.

    :param response: UTF-8 encoded JSON string
    :return dict: decoded UTF-8 encoded JSON string as a dict
    """
    return json.loads(response.decode('utf-8'))


def create_table_message(service_name, model_instance: DataModel):
    """
    Creates a message to be sent to the storage service used to define tables
    for modelled data.

    :param service_name: name of the service that is registering a model
    :param model_instance: actual data model instance, descendant of DataModel
    :return: JSON formatted, UTF-8 encoded, string
    """
    LOGGER.debug(f"Creating table: {model_instance}")

    message = {
        "owner": service_name,
        "table_name": model_instance.__class__.__name__,
        "fields": {}
    }

    fields = model_instance.get_model_fields()

    for column, field in fields:
        field_string = make_field_string(field)
        LOGGER.debug(f"Field string: {field_string}")

        message["fields"].update({
            column: field_string
        })

    LOGGER.debug(f"Resulting message: "
                 f"{json.dumps(message, indent=4, sort_keys=True)}")

    return json.dumps(message, sort_keys=True).encode('utf-8')


def make_field_string(field):
    """
    Creates a field string to be included in a CREATE table message.

    Normally, a field string is just the string representation of the field's
    class name. In some other cases, special handling is put on:

    1. Relation fields (FK, One to one, etc): can also be the key for a table
        ForeignKey(RelatedClass)
        OneToOne(RelatedClass, KEY)
    2. Enums
        Enum(data type)

    :param field: one of the fields defined under storage.definitions.fields
    :return: a field's string representation
    """
    field_name = field.__class__.__name__

    if has_relation(field):
        field_relation = field.cls.__name__

        key = ""
        if is_key(field):
            key = ", KEY"

        return f"{field_name}({field_relation}{key})"

    elif is_enum(field):
        field_type = type(field.options[1]).__name__

        return f"{field_name}({field_type})"

    return field_name
