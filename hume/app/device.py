import logging

from app.abc import App


LOGGER = logging.getLogger(__name__)


class Device(App):
    def pre_start(self):
        LOGGER.info("Device pre_start")

    def start(self):
        LOGGER.info("Device start")

    def post_start(self):
        LOGGER.info("Device post_start")

    def pre_stop(self):
        LOGGER.info("Device pre_stop")

    def stop(self):
        LOGGER.info("Device stop")

    def post_stop(self):
        LOGGER.info("Device post_start")
