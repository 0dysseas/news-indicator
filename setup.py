#!/usr/bin/python

import os

from distutils.core import setup

# Package meta-data.
NAME = 'News Indicator'
DESCRIPTION = 'Linux app indicator that retrieves news from top media outlets'
URL = 'https://github.com/0dysseas/news-indicator'

# Load the package's __version__.py module as a dictionary.
about = {}
with open(os.path.join(here, NAME, '__version__.py')) as f:
    exec(f.read(), about)


def find_resources(resource_dir):
    target_path = os.path.join('/usr/share/newsindicator', resource_dir)
    resource_names = os.listdir(resource_dir)
    resource_list = [os.path.join(resource_dir, file_name) for file_name in resource_names]
    return target_path, resource_list


setup(name=NAME,
      version=about['__version__'],
      description=DESCRIPTION,
      url=URL,
      license='GNU Lesser General Public License v3.0',
      packages=['newsindicator'],
      data_files=[
          ('/usr/share/applications', ['newsindicator.desktop']),
          find_resources('assets')],
      scripts=['bin/newsindicator']
)