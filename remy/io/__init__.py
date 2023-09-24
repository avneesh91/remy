import questionary
from remy.io.constants import HANDLER_ACTIONS
from remy.domain.service_locater import ServiceLocater
from remy.io.handlers.record_addition_handler import RecordAdditionHandler

class CommandLineIOHandler:

    def __init__(self, service_locater: ServiceLocater):
        self._handlers = {}
        self._handlers[HANDLER_ACTIONS.ADD_RECORD] = RecordAdditionHandler(service_locater)

    def run(self):
        action = questionary.select(
                "Select action to do",
                choices=self._handlers.keys()).ask()

        instance = self._handlers[action]

        instance.run_input_prompt()
        instance.run()


def get_command_line_io_handler(service_locater):
    return CommandLineIOHandler(service_locater)
