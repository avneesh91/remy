from remy.io import get_command_line_io_handler
from remy.domain import get_service_locator

service_locater = get_service_locator()
io_handler = get_command_line_io_handler(service_locater)

io_handler.run()
