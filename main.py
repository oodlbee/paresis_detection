from application.win_main import Application
from configparser import ConfigParser

if __name__ == "__main__":
    app_config = ConfigParser()
    app_config.read('application/app_config.ini')
    config = ConfigParser()
    config.read('computation/comp_config.ini')
    application = Application(app_config, config)
    application.mainloop()