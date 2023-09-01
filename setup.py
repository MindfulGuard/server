from setuptools import setup, find_packages

setup(
    name='mypass',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'asyncpg',
        'pycryptodome',
        'fastapi[all]'
    ],
    dependency_links = [
        'lib/secure_remote_passwordpy'
    ]
)