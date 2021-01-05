import logging

from microserviceutil.lazy.lazy_frontend import LazyFrontendUpdater
from microserviceutil.lazy.lazy_mongoose import LazyMongoose


class Lazy:
    try:
        JOBS = {
            "mongoose": LazyMongoose,
            "frontend": LazyFrontendUpdater
        }

        def __init__(self, args):
            # check the number of arguments
            if len(args) >= 2:
                self.job_name = args[0]
                self.params = args[1:]

                if self.job_name in self.JOBS:
                    job = self.JOBS[self.job_name](self.params)
                    job.run_job()
    except Exception as error:
        logging.error(error)
