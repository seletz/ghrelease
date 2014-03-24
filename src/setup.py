# -*- coding: utf-8 -*-
"""
Setup script for the ghrelease tool
"""
import os
from setuptools import setup, find_packages

from ghrelease import __version__


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = __version__

long_description = (
    read('../readme.rst')
    )

setup(name='ghrelease',
      version=version,
      description="A GitHub release helper",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='',
      author='Stefan Elethofer',
      author_email='se@nexiles.com',
      license='public domain',
      packages=find_packages('.', exclude=['ez_setup']),
      url='https://github.com/seletz/ghrelease',
      download_url='https://github.com/seletz/ghrelease/releases',
      package_dir={'': '.'},
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'colorama',
                        'docopt',
                        'blessings',
                        'github3.py'
                        # -*- Extra requirements: -*-
                        ],
      entry_points={
          'console_scripts': [
              'ghrelease = ghrelease:main'
              ]
          }
      )
