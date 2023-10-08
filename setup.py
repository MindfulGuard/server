from setuptools import setup, find_packages

setup(
    name='mindfulguard',
    version='0.0.0',
    packages=find_packages(),
    pythonpath = [
        ".",
        "mindfulguard",
    ],
    install_requires=[
        'pyotp',
        'asyncpg',
        'pycryptodome',
        'fastapi[all]',
        'tomli',
        'pytest',
        'pytest-asyncio',
        'cryptography',
        'minio' 
    ],
)