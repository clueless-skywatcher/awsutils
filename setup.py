from setuptools import setup, find_packages

setup(
    name = 'awsutils',
    version = '1.0',
    description = 'OOP utilites for accesssing AWS services',
    packages = find_packages(),
    install_requires = [
        'boto3'
    ]
)
