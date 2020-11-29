import logging
import os

from clients.base_micro_client import BaseMicroClient
from migrations.migrate import Migrate
from services.config_service import ConfigService


class MigrateMongoProToDev(Migrate):

    def __init__(self, params):
        super().__init__(params)

        # get info from params
        if len(params) > 2:
            self.project_id, self.database, self.collection = params
        else:
            self.project_id, self.database, = params

        # env vars
        self.env_from = os.environ.get('FROM', None)
        self.prune = os.environ.get('PRUNE', 'False').lower() == 'true'

        # services configuration
        if self.project_id:
            ConfigService().project_id = self.project_id

        # clients
        self.bmc_from = BaseMicroClient(self.env_from)
        self.bmc = BaseMicroClient()

    def run_job(self):
        self.migrate_collection(self.database, self.collection)

    def migrate_collection(self, database, collection):
        logging.info(f'Migrating the collection -> {collection.upper()}')
        migration = self.bmc_from.get_migrations_items(database, collection)

        # comprobamos cuales podemos migrar
        migrated = []
        for item in migration.items:
            logging.info(item)
            migrated += self.__should_be_migrated(collection, item)

        if migrated:
            if self.prune:
                self.bmc.delete_items(database, collection)
            self.bmc.save_migration_items(database, collection, migrated)

    def __should_be_migrated(self, collection, item):
        result = [item]
        # if collection == 'placeholder':
        #     if 'key_property_values' and item['key_property'] not in ['key_property_values']:
        #         result = []
        return result
