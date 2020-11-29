import logging
import os


class Migrate:

    def __init__(self, params):
        # super().__init__(params)
        logging.info(params)

        # get env var info
        self.env = os.environ.get('ENV', 'dev')

    def end_job(self):
        pass
