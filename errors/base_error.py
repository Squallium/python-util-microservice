import logging
import sys


class BaseError:
    CONFIG_FILE_NOT_FOUND = 1000

    SWITCHER = {
        CONFIG_FILE_NOT_FOUND: 'Config file cannot be found'
    }

    def terminate(self, code, err=None):
        if err:
            logging.error(err)
        logging.error(f'{code}: {self._switcher().get(code, "")}')
        sys.exit(code)

    def _switcher(self):
        return self.SWITCHER
