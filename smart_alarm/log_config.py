

# logging configuration
log_file = "logfiles/smala.log"
logging_level = 'DEBUG'

format_log_file = "%(asctime)s :: %(levelname)s :: " \
                  "%(funcName)s in %(filename)s (l:%(lineno)d) :: %(message)s"
format_console = "%(levelname)s - %(filename)s l:%(lineno)d - %(message)s"
logging_dict = {
    'version': 1,
    'disable_existing_loggers': True,   # important to set True to suppress existing loggers from other modules
    'loggers': {
        '': {
            'level': logging_level,
            'handlers': ['console', 'file'],
        },
    },
    'formatters': {
        'format_for_file': {'format': format_log_file, 'datefmt': '%Y-%m-%d %H:%M:%S'},
        'format_for_console': {'format': format_console, 'datefmt': '%m-%d %H:%M:%S'}
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'format_for_console',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'format_for_file',
            'filename': log_file,
            'maxBytes': 500000,
            'backupCount': 20
        }
    },
}
