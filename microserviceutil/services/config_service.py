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

        # attributes
        self.__configs = {}
        self._project_id = None

    def __load_cfg(self, env=None):
        env = env if env else self.__default_env
        try:
            with open("microserviceutil/configs/{0}/config.yml".format(env), 'r') as ymlfile:
                self.__configs[env] = yaml.load(ymlfile, Loader=yaml.FullLoader)
        except FileNotFoundError as fnfe:
            BaseError().terminate(BaseError.CONFIG_FILE_NOT_FOUND)

    def __cfg(self, env=None):
        env = env if env else self.__default_env
        if env not in self.__configs:
            self.__load_cfg(env)
        return self.__configs[env]

    def __project_cfg(self, env=None):
        return self.__cfg(env)[ConfigService.PROJECTS][self.project_id]

    @property
    def project_id(self):
        return self._project_id

    @project_id.setter
    def project_id(self, value):
        self._project_id = value

    def migrations_endpoint(self, env=None):
        return self.__project_cfg(env)[self.MIGRATIONS_ENDPOINT]
