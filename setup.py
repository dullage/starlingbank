from setuptools import setup
import starling

setup(
    name='starling',
    version=starling.__version__,
    description='A python package that provides limited access to the Starling bank API.',  # noqa
    url='https://github.com/Dullage/starling',
    author='Adam Dullage',
    author_email='adam@dullage.com',
    license='MIT',
    packages=['starling'],
    install_requires=[
        'requests'
    ],
)
