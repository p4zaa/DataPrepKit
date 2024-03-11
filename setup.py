from setuptools import setup, find_packages

setup(
    name='DataPrepKit',
    version='0.1a',
    description='Library kit for Thai language preprocessing.',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'pythainlp',
        'tqdm',
        'polars>=0.19.0',
        'xlsx2csv',
    ],
)
