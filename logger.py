import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import os


class FileNameFilter(logging.Filter):
    def __init__(self, filename):
        super().__init__()
        self.filename = os.path.basename(filename)

    def filter(self, record):
        record.filename = self.filename
        return True


class LoggerClass:
    def __init__(self, logger_name, log_file_name):
        # Define API log level
        API = 25
        # "Register" new logging level
        logging.addLevelName(API, 'API')
        # Verify
        assert logging.getLevelName(API) == 'API'

        # Ensure the logs directory exists
        logs_directory = 'logs'
        os.makedirs(logs_directory, exist_ok=True)

        # Get the current date for the log file name
        current_date = datetime.now().strftime('%m-%d-%y')

        # Create a TimedRotatingFileHandler
        file_handler = TimedRotatingFileHandler(os.path.join(logs_directory, f'{current_date} - {log_file_name}.log'),
                                                when="midnight", interval=1, backupCount=30)
        file_handler.setLevel(logging.INFO)

        # Create a formatter and add it to the handler
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s] - %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger = logging.getLogger(logger_name)
        if not self.logger.handlers:  # This line checks if the logger already has a handler
            self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.INFO)

    def log(self, level, message, filename):
        # Add the filename filter
        filename_filter = FileNameFilter(filename)
        self.logger.addFilter(filename_filter)

        if level == 'debug':
            self.logger.debug(message)
        elif level == 'info':
            self.logger.info(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        elif level == 'critical':
            self.logger.critical(message)
        elif level == 'api':
            self.logger.log(25, message)  # 25 is the level number for 'API'
        self.logger.removeFilter(filename_filter)  # Remove the filter after logging


short_log = LoggerClass('short_logger', 'dhcp_server_lease_runner')
whole_log = LoggerClass('whole_logger', 'whole_dhcp_server_lease_runner')


def log_message(level, message, filename=__file__):
    short_log.log(level, message, filename)
    whole_log.log(level, message, filename)


def log_message_short(level, message, filename=__file__):
    short_log.log(level, message, filename)


def log_message_whole(level, message, filename=__file__):
    whole_log.log(level, message, filename)
