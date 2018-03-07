import os

project_path = os.environ['smart_alarm_path']

# logging configuration
log_file = str(project_path) + "/logfiles/smala.log"
logging_level = 'DEBUG'

format_log_file = "%(asctime)s :: %(levelname)s :: " \
                  "%(funcName)s in %(filename)s (l:%(lineno)d) :: %(message)s"
format_console = "%(asctime)s - %(levelname)s - %(filename)s l:%(lineno)d - %(message)s"
logging_dict = {
    'version': 1,
    'disable_existing_loggers': True,   # important to set True to suppress existing loggers from other modules
    'loggers': {
        '': {
            'level': logging_level,
            'handlers': ['console', 'file'],
        },
        #'__main__': {
        #    'level': logging_level,
        #    'handlers': ['console', 'file'],
        #},
        #'modules.sounds': {
        #    'level': logging_level,
        #    'handlers': ['console', 'file'],
        #},
        #'modules.xml_data': {
        #    'level': logging_level,
        #    'handlers': ['console', 'file'],
        #},
        #'modules.led': {
        #    'level': logging_level,
        #    'handlers': ['console', 'file'],
        #},
        #'modules.display_class': {
        #    'level': logging_level,
        #    'handlers': ['console', 'file'],
        #},

    },
    'formatters': {
        'format_for_file': {'format': format_log_file, 'datefmt': '%Y-%m-%d %H:%M:%S'},
        'format_for_console': {'format': format_console, 'datefmt': '%m-%d %H:%M:%S'}
    },
    'handlers': {
        'console': {
            'level': logging_level,
            'class': 'logging.StreamHandler',
            'formatter': 'format_for_console',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'level': logging_level,
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'format_for_file',
            'filename': log_file,
            'maxBytes': 500000,
            'backupCount': 20
        }
    },
}
