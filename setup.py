from setuptools import setup

setup(
    name='starlingbank',
    version="3.1",
    description='An unofficial python package that provides access to parts of the Starling bank API. Designed to be used for personal use (i.e. using personal access tokens).',  # noqa
    url='https://github.com/Dullage/starlingbank',
    author='Adam Dullage',
    author_email='adam@dullage.com',
    license='MIT',
    packages=['starlingbank'],
    install_requires=[
        'requests'
    ],
)
