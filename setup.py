#! /usr/bin/env python

from setuptools import setup, find_packages

setup(name="podiff",
      version="0.1",
      author="Rory McCann",
      author_email="rory@technomancy.org",
      py_modules=['podiff'],
      install_requires=['polib'],
      license = 'GPLv3',
      description = 'Sematically compare two .po/gettext files for differences, ignoring, ordering, whitespace, comments, etc.',
      entry_points = {
          'console_scripts': [
              'podiff = podiff:main',
          ]
      },
)
