from setuptools import setup, find_packages

setup(
    name='mindfulguard',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'pyotp',
        'asyncpg',
        'pycryptodome',
        'fastapi[all]',
        'pydantic-async-validation',
        'pytest',
        'pytest-asyncio',
        'cryptography',
        'minio' 
    ],
)