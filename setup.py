import os
import shutil

from setuptools import setup

scripts = ['bin/mkstm32']

if os.name == 'nt':
  shutil.copy('bin/mkstm32', 'bin/mkstm32.py')
  scripts = ['bin/mkstm32.py']

setup(
  name='mkstm32',
  version='1.3.0',
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
