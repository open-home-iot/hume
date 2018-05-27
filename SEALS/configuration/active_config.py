from configuration.configurations import *


class Configuration:
    config_dict = {
        0: True,
        1: True,
    }

    def set_config_item(self, key, value):
        self.config_dict[key] = value

    def get_config_item(self, key):
        return self.config_dict[key]

    def is_config_valid(self):
        return self.config_dict is not None

    def get_config(self):
        return self.config_dict


true = ['1', 'True', 'true', True]
false = ['0', 'False', 'false', False]
active_config = Configuration()


def update_config(new_config):
    active_config.set_config_item(ALARM, new_config['alarm_state'] in true)
    active_config.set_config_item(PICTURE_MODE, new_config['picture_mode'] in true)

    print("CONFIGURATIONS: New config:", active_config.get_config())
