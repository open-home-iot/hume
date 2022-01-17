import logging

from app.abc import App
from util.storage import DataStore

LOGGER = logging.getLogger(__name__)


class HintApp(App):

    def __init__(self, cli_args, storage: DataStore):
        self.cli_args = cli_args
        self.storage = storage

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
        LOGGER.info("Device post_stop")
