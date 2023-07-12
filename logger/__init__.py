import os
from logger.utils.events import Events

if os.environ.get('RUN_MAIN', None) != 'true':
    default_app_config = 'logger.apps.LoggerConfig'

API_LOGGER_SIGNAL = Events()