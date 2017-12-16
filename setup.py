#!/usr/bin/python

# from distutils.core import setup
from setuptools import setup

# Package meta-data.
NAME = 'newsindicator'
DESCRIPTION = 'Linux app indicator that retrieves news from top media outlets'
URL = 'https://github.com/0dysseas/news-indicator'

REQUIRED = [
    'requests', 'APScheduler', 'notify2',
]

setup(name=NAME,
      version='1.0.0',
      description=DESCRIPTION,
      url=URL,
      license='GNU Lesser General Public License v3.0',
      packages=['newsindicator'],
      install_requires=REQUIRED,
      data_files=[
          ('/usr/share/applications', ['newsindicator.desktop']),
          ('/usr/share/icons', ['newsindicator_icon.png'])
          ],
      package_data={'newsindicator': ['assets/*']},
      scripts=['bin/newsindicator']
)