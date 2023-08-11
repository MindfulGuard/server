from setuptools import setup, find_packages

setup(
    name='mypass',
    version='0.1.0',
    description='Key master',
    author='MyPass',
    author_email='null',
    packages=find_packages(),
    install_requires=[
        'asyncpg',
        'pycryptodome'
    ],
)