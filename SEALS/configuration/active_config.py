class Configuration:
    config_dict = None

    def set_config_item(self, key, value):
        self.config_dict[key] = value

    def get_config_item(self, key):
        return self.config_dict[key]

    def is_config_valid(self):
        return self.config_dict is not None

    def get_config(self):
        return self.config_dict


active_config = Configuration()
