from setuptools import setup

setup(
  name='mkstm32',
  version='1.0.4',
  description='Upload, debug and compile STM32CubeMX Makefile projects',
  url='https://github.com/adzierzanowski/mkstm32',
  author='Aleksander Dzierżanowski',
  author_email='a.dzierzanowski1@gmail.com',
  license='MIT',
  packages=['mkstm32'],
  install_requires=['pyserial'],
  scripts=['bin/mkstm32'],
  zip_safe=False
)
