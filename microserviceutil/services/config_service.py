import logging
import os

import yaml

from microserviceutil.errors.base_error import BaseError
from microserviceutil.services.base_service import BaseService


class ConfigService(metaclass=BaseService):
    PROJECTS = 'projects'
    MIGRATIONS_ENDPOINT = 'migrations_endpoint'

    def __init__(self) -> None:
        super().__init__()

        # env vars
        self.__default_env = os.environ.get('ENV', 'dev')
        self.__project_id = os.environ.get('PROJECT_ID', None)

        # attributes
        self.__configs = {}

    def __load_cfg(self, env=None):
        env = env if env else self.__default_env
        try:
            with open("./configs/{0}/config.yml".format(env), 'r') as ymlfile:
                self.__configs[env] = yaml.load(ymlfile, Loader=yaml.FullLoader)
        except FileNotFoundError as fnfe:
            BaseError().terminate(BaseError.CONFIG_FILE_NOT_FOUND)

    def __cfg(self, env=None):
        env = env if env else self.__default_env
        if env not in self.__configs:
            self.__load_cfg(env)
        return self.__configs[env]

    def _project_cfg(self, env=None, project_id=None):
        logging.info(self.__cfg(env)[ConfigService.PROJECTS])
        logging.info(self._project_id(project_id))
        return self.__cfg(env)[ConfigService.PROJECTS][self._project_id(project_id)]

    def _project_id(self, project_id=None):
        return project_id if project_id else self.__project_id

    def migrations_endpoint(self, env=None):
        return self._project_cfg(env, 'vine_micro')[self.MIGRATIONS_ENDPOINT]
