from setuptools import setup
import starlingbank

setup(
    name='starlingbank',
    version=starlingbank.__version__,
    description='A python package that provides limited access to the Starling bank API.',  # noqa
    url='https://github.com/Dullage/starlingbank',
    author='Adam Dullage',
    author_email='adam@dullage.com',
    license='MIT',
    packages=['starlingbank'],
    install_requires=[
        'requests'
    ],
)
