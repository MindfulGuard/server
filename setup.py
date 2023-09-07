from setuptools import setup, find_packages

setup(
    name='mypass',
    version='0.0.0',
    packages=find_packages(),
    install_requires=[
        'asyncpg',
        'pycryptodome',
        'fastapi[all]',
        'tomli',
        'pytest'
    ],
)