from setuptools import find_packages, setup

setup(
    name='pgMigrationMgr',
    packages=find_packages(include=['pgMigrationMgr']),
    version='0.0.2',
    description='A small library to run sql files on postgres',
    author_email='devlpalomo@gmail.com',
    author='Lucas Palomo',
    license='MIT',
    setup_requires=['psycopg2-binary'],
)
