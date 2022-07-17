# Postgres Migration Manager

----

## Install

To install **_pgMigrationManager_** run the following command

```bash
pip3 install git+https://github.com/Lucas-Palomo/pgMigrationMgr 
```

## About

Migration Manager is a way to run .sql scripts.

* Folders and Files must be named starting with a serial sequence (like django migrations)
  * Example 001, 002, 003
* Files must be named ending in **_.up.sql_** or **_.down.sql_**
  * **_.up.sql_**
    * Files are executed to create database
  * **_.down.sql_**
    * Files are executed to destroy database

## Arguments

The following args are accepted
* **is_separated_by_dir** = use True if migrations directory has another directories inside
* **dir_like_schema** = use True if each directory inside migrations is a database schema
* **verbose** = logs all executions if true


## Examples

---
### Example I

Migrations folder content:
* 001.create_table1.up.sql
* 001.drop_table1.down.sql
* 002.create_table2.up.sql
* 002.drop_table2.down.sql

```python
from pgMigrationMgr import MigrationMgr

pg_connection = # Your postgres connection
migrations_path = # Your migrations path | Default is the project folder ./migrations

migration_mgr = MigrationMgr(conn=pg_connection, migrations_path=migrations_path)

migration_mgr.create() # to create your database
migration_mgr.destroy() # to destroy your database

```


>The create function executes sql files in this order:
>* 001.create_table1.up.sql
>* 002.create_table2.up.sql

>The destroy function executes sql files in this order:
>* 002.drop_table2.down.sql
>* 001.drop_table1.down.sql

---

### Example II

Migrations folder content:
* 001.create_table1.up.sql
* 002.create_table2.up.sql
* 001.drop_tables.down.sql

```python
from pgMigrationMgr import MigrationMgr

pg_connection = # Your postgres connection
migrations_path = # Your migrations path | Default is the project folder ./migrations

migration_mgr = MigrationMgr(conn=pg_connection, migrations_path=migrations_path)

migration_mgr.create() # to create your database
migration_mgr.destroy() # to destroy your database

```


>The create function executes sql files in this order:
>* 001.create_table1.up.sql
>* 002.create_table2.up.sql

>The destroy function executes sql files in this order:
>* 001.drop_tables.down.sql

---

### Example III

Migrations folder content:
* 0001_tables
  * 001.create_table1.up.sql
  * 002.create_table2.up.sql
  * 001.drop_tables.down.sql
* 0002_views
  * 001.create_view.up.sql
  * 001.drop_view.down.sql

```python
from pgMigrationMgr import MigrationMgr

pg_connection = # Your postgres connection
migrations_path = # Your migrations path | Default is the project folder ./migrations

migration_mgr = MigrationMgr(conn=pg_connection, 
                             migrations_path=migrations_path,
                             is_separated_by_dir=True)

migration_mgr.create() # to create your database
migration_mgr.destroy() # to destroy your database

```


>The create function executes sql files in this order:
>* 0001_tables
>  * 001.create_table1.up.sql
>  * 002.create_table2.up.sql
>* 0002_views
>  * 001.create_view.up.sql

>The destroy function executes sql files in this order:
>* 0002_views
>  * 001.drop_view.down.sql
>* 0001_tables
>  * 001.drop_tables.down.sql

---

### Example IV

Migrations folder content:
* 0001_schema1
  * 001.create_table1.up.sql
  * 001.drop_table1.down.sql
* 0002_schema2
  * 001.create_table2.up.sql
  * 001.drop_table2.down.sql

```python
from pgMigrationMgr import MigrationMgr

pg_connection = # Your postgres connection
migrations_path = # Your migrations path | Default is the project folder ./migrations

migration_mgr = MigrationMgr(conn=pg_connection, 
                             migrations_path=migrations_path,
                             is_separated_by_dir=True,
                             dir_like_schema=True)

migration_mgr.create() # to create your database
migration_mgr.destroy() # to destroy your database

```


>The create function executes sql files in this order:
>* 0001_schema1
>  * 001.create_table1.up.sql
>* 0002_schema2
>  * 001.create_table2.up.sql
> 
> On database two schemas is created, schema1 and schema2

>The destroy function executes sql files in this order:
>* 0002_schema2
>  * 001.drop_table2.up.sql
>* 0001_schema1
>  * 001.drop_table1.up.sql
>
> The Destroy function cannot drop the schemas