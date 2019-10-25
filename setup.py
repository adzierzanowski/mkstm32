import os
import shutil

from setuptools import setup

from mkstm32.version import __version__

scripts = ['bin/mkstm32']

if os.name == 'nt':
  shutil.copy('bin/mkstm32', 'bin/mkstm32.py')
  scripts = ['bin/mkstm32.py']

setup(
  name='mkstm32',
  version=__version__,
  description='Upload, debug and compile STM32CubeMX Makefile projects',
  url='https://github.com/adzierzanowski/mkstm32',
  author='Aleksander Dzierżanowski',
  author_email='a.dzierzanowski1@gmail.com',
  license='MIT',
  packages=['mkstm32'],
  install_requires=['pyserial'],
  scripts=scripts,
  zip_safe=False
)

