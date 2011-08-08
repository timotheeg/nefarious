"""
setup.py for nefarious
"""
__author__ = "Timothee Groleau"
__copyright__ = "Copyright 2011"
__email__ = ""

from setuptools import setup, find_packages

version = "0.1"
setup(name='nefarious',
     version=version,
     description="Nikon NEF File Parser"
     long_description="Manipulates your Nikon NEF files to (amongst other things) change the embedded jpeg thumbnail",
     packages=find_packages(exclude=['ez_setup']),
     include_package_data=True,
     zip_safe=False,
     install_requires=[
         'setuptools',
         ],
     entry_points={
         'console_scripts': [
             'nef-cli = nefarious.main:main',
             ]
        }
     )

