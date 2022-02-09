import logging


class Logger:
    instance = None

    def __new__(cls):
        if not Logger.instance:
            formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            filepath = 'logs.txt'
            info_file_handler = logging.FileHandler(filepath)
            info_file_handler.setLevel(logging.INFO)
            info_file_handler.setFormatter(formatter)

            Logger.instance = logging.getLogger('logger')
            Logger.instance.setLevel(logging.DEBUG)
            Logger.instance.addHandler(info_file_handler)
            Logger.instance.addHandler(console_handler)

        return Logger.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, val):
        return setattr(self.instance, name, val)
