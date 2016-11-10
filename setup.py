from distutils.core import setup

with open('README.txt', 'r') as f:
    readme = f.read()

setup(
    name='netconnect',
    version='0.1',
    packages=['netconnect',],
    license='GNU GENERAL PUBLIC LICENSE Version 3',
    long_description=readme,
)
