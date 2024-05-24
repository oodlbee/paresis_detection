from application.win_main import Application
from configparser import ConfigParser
from pathlib import Path
import logging


if __name__ == "__main__":
    # initializing configs
    app_config = ConfigParser()
    app_config.read('application/app_config.ini')
    
    # initialize output applocation logger
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(filename)s/%(funcName)s] - %(levelname)s - %(message)s')

    # initialize applocation logger
    app_logger_folder = Path(app_config['internal.files']['applications_loggers'][1:-1]).absolute()
    app_logger = logging.getLogger('app_logger')
    app_handler = logging.FileHandler(str(app_logger_folder / Path('app_logger.log')), mode='w')
    format = logging.Formatter('%(asctime)s [%(filename)s/%(funcName)s] - %(levelname)s - %(message)s')
    app_handler.setFormatter(format)
    app_logger.addHandler(app_handler)
    app_logger.setLevel(logging.DEBUG)


    # run application
    application = Application(app_config)
    application.mainloop()