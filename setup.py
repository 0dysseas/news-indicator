#!/usr/bin/python

import os

from distutils.core import setup
from distutils import sysconfig

# Package meta-data.
NAME = 'newsindicator'
DESCRIPTION = 'Linux app indicator that retrieves news from top media outlets'
URL = 'https://github.com/0dysseas/news-indicator'


def find_resources(resource_dir):
    dist_package_path = sysconfig.get_python_lib()
    target_path = os.path.join(dist_package_path, NAME, resource_dir)
    resource_names = os.listdir(resource_dir)
    resource_list = [os.path.join(resource_dir, file_name) for file_name in resource_names]
    return target_path, resource_list


setup(name=NAME,
      version='1.0.0',
      description=DESCRIPTION,
      url=URL,
      license='GNU Lesser General Public License v3.0',
      packages=['newsindicator'],
      # package_dir={'newsindicator': 'newsindicator'},
      # package_data={'newsindicator': ['assets']},
      include_package_data=True,
      data_files=[
          ('/usr/share/applications', ['newsindicator.desktop']),
          # find_resources('assets'),
          ],
      # package_data={
      #     # If any package contains *.txt or *.rst files, include them:
      #     '': ['*.png', '*.txt']
      # },
      scripts=['bin/newsindicator']
)