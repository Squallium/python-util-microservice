import logging
import os

import requests

from services.config_service import ConfigService
from utils.response import BaseModel, Response


class MigrationModel(BaseModel):

    def __init__(self, data) -> None:
        self.items: [] = None

        super().__init__(data)


class BaseMicroClient:

    def __init__(self, env=None) -> None:
        super().__init__()

        # different env possibility
        self.env = env

    def get_migrations_items(self, database: str, collection: str) -> MigrationModel:
        migration: MigrationModel = None

        endpoint = os.path.join(ConfigService().migrations_endpoint(self.env), database, collection)
        params = {}
        rsp = requests.get(endpoint, params)
        response = Response.from_request(rsp, model_class=MigrationModel)

        if response.is_ok:
            migration: MigrationModel = response.payload
            logging.info(migration)
        else:
            logging.error(response.payload)

        return migration

    def save_migration_items(self, database: str, collection: str, items: []):
        endpoint = os.path.join(ConfigService().migrations_endpoint(self.env), database, collection)
        headers = {'Content-type': 'application/json'}
        body = items

        rsp = requests.post(endpoint, json=body, headers=headers)

        response = Response.from_request(rsp)  # , model_class=ProductModel)

        if response.is_ok:
            logging.info(response.payload)
        else:
            if response.payload['code'] != 11000:
                logging.error(response.payload)