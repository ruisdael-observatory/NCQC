'''
File to set up the python library.
'''

from setuptools import find_packages, setup

setup(
    name='netcdfqc',
    packages=find_packages(include=['netcdfqc']),
    version='0.1.0',
    description='Library to perform quality control on netCDF files.',
    author='Noky Soekarman, Jesse Vleeschdraager, Mels Lutgerink, Ella Milinović, Vasil Chirov',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)
