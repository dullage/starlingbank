from setuptools import setup

setup(
    name='starlingbank',
    version="2.0dev",
    description='A python package that provides limited access to the Starling bank API.',  # noqa
    url='https://github.com/Dullage/starlingbank',
    author='Adam Dullage',
    author_email='adam@dullage.com',
    license='MIT',
    packages=['starlingbank'],
    install_requires=[
        'requests',
        'uuid',
        'json'
    ],
)
