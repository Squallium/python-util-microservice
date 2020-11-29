import logging
import os
import sys

from lazy.lazy import Lazy
from migrations.migrations import Migrations


class PythonUtil:
    MODULES = {
        "lazy": Lazy,
        "migrations": Migrations
    }

    def __init__(self):
        paused = os.environ.get('PAUSED', 'False').lower()
        if paused == 'true':
            logging.info("Process on pause")
            sys.exit(0)

        # check de number of arguments
        if len(sys.argv) >= 3:
            self.module = sys.argv[1]
            self.arguments = sys.argv[2:]

    def run_job(self):
        if self.module in self.MODULES.keys():
            mod = self.MODULES[self.module](args=self.arguments)
            logging.info(mod)


logging.basicConfig(level=logging.INFO)
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.CRITICAL)
c = PythonUtil()
c.run_job()
