from setuptools import find_packages, setup

install_requires = [
    'google-api-python-client>=1.12.8',
    'google-auth-httplib2>=0.0.4',
    'google-auth-oauthlib>=0.4.2',
    'PyYAML==5.3.1'
]

version = "1.0.0"

setup(
    name='python-util-microservice',
    packages=find_packages(),
    version=version,
    description='Python Utilities for the Microservices',
    author='Borja Refoyo Ruiz',
    url='https://github.com/Squallium/python-util-microservice',
    install_requires=install_requires,
)
