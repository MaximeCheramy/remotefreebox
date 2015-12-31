# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='remotefreebox',
    version='0.2',

    description='A Python module to control a Freebox v6 remotely',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/MaximeCheramy/remotefreebox',

    # Author details
    author='Maxime Chéramy and Francois Guibert',
    author_email='maxime.cheramy@gmail.com',

    # Choose your license
    license='BSD',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    # What does your project relate to?
    keywords='freebox remote control rudp hid',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

    install_requires=['zeroconf>=0.17']
)
