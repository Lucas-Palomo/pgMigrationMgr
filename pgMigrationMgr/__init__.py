import os
import sys
from pathlib import Path as __Path__
from typing import List as __List__
from psycopg2._psycopg import connection as __conn__, cursor as __cur__


class MigrationMgr:
    """ Execute all migrations found in path
            - Migrations file endings with **.up.sql** are executed to create
            - Migrations file endings with **.down.sql** are executed to destroy
        :raw-html:`<div style="margin: 3px;">`

        The **kwargs accepts the following instructions
            - **is_separated_by_dir** = use True if migrations directory has another directories inside
            - **dir_like_schema** = use True if each directory inside migrations is a database schema
            - **verbose** = logs all executions if true


        :raw-html:`</div>`
        ----
        :param conn: Postgres Connection
        :param migrations_path: Default Path is a folder inside project called migrations
        :param configs: additional configs to run your migrations
    """

    def __init__(self,
                 conn: __conn__,
                 migrations_path: str = "{}/migrations/".format(__Path__().resolve().__str__()),
                 **kwargs):
        self.__conn = conn
        self.__migrations_path: str = migrations_path
        self.__up: dict = {'public': []}
        self.__down: dict = {'public': []}
        self.__configs = kwargs

        if __Path__(self.__migrations_path).exists():
            if __Path__(self.__migrations_path).is_dir():
                if self.__configs.get('is_separated_by_dir', False) and self.__configs.get('dir_like_schema', False):
                    for directory in sorted(os.listdir(self.__migrations_path)):
                        self.__get_all_migrations(directory=directory, is_schema=True)
                elif self.__configs.get('is_separated_by_dir', False):
                    for directory in sorted(os.listdir(self.__migrations_path)):
                        self.__get_all_migrations(directory=directory)
                else:
                    self.__get_all_migrations()
            else:
                sys.exit("migrations path is not a dir")
        else:
            sys.exit("migrations path not found")

        for schema in list(self.__up.keys()):
            self.__up[schema] = sorted(self.__up[schema])
            self.__down[schema] = list(reversed(sorted(self.__down[schema])))

    def __execute_migration(self, schema: str, migration: str):
        schema_name = str(schema)

        if "_" in schema:
            schema_name = str(schema).split("_", 1)[1]

        try:
            cur: __cur__ = self.__conn.cursor()

            cur.execute("CREATE SCHEMA IF NOT EXISTS {}".format(schema_name))
            self.__conn.commit()

            cur.execute("SET SCHEMA '{}'".format(schema_name))
            self.__conn.commit()

            query = "".join(open(migration, "r").readlines())
            cur.execute(query)
            self.__conn.commit()
            cur.close()
        except Exception as exception:
            sys.exit(exception)

    def create(self):
        for schema in self.__up.keys():
            for migration in self.__up[schema]:
                self.__verbose(message="executing schema ({})\n\t up -> {}", args=[schema, migration])
                self.__execute_migration(schema, migration)

    def destroy(self):
        for schema in reversed(sorted(self.__down.keys())):
            for migration in self.__down[schema]:
                self.__verbose(message="executing schema ({})\n\t down -> {}", args=[schema, migration])
                self.__execute_migration(schema, migration)

    def __verbose(self, message: str, args: __List__[str]):
        if self.__configs.get('verbose', False):
            print(message.format(*args))

    def __migration_reasoner(self, migration: str, schema: str = 'public'):
        if migration.endswith("up.sql"):
            if schema not in self.__up:
                self.__up[schema] = []
            self.__up[schema].insert(0, migration)
        if migration.endswith("down.sql"):
            if schema not in self.__down:
                self.__down[schema] = []
            self.__down[schema].insert(0, migration)

    def __get_all_migrations(self, directory: str | None = None, is_schema: bool = False):
        path = self.__migrations_path
        if directory is not None:
            path = "{}/{}".format(self.__migrations_path, directory)

        for migration in os.listdir(path=path):
            if is_schema:
                self.__migration_reasoner(migration="{}/{}".format(path, migration), schema=directory)
            else:
                self.__migration_reasoner(migration="{}/{}".format(path, migration))
