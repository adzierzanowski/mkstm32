import sys

class Version:
  major = 1
  minor = 0
  patch = 0
  date = '14 Jan 2019'

  @staticmethod
  def str_():
    return '{}.{}.{}'.format(Version.major, Version.minor, Version.patch)

  @staticmethod
  def print(cli):
    cli.print('Version {} ({})'.format(Version.str_(), Version.date))
    sys.exit()
