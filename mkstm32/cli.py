import os
import sys
import subprocess

from mkstm32.option import Option
from mkstm32.stlink import STLink

# Checks for ANSI escape codes support
def formatter(func):
  def wrapper(text):
    posix_support = os.name == 'posix' and hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    win_support = os.name == 'nt' and 'ANSICON' in os.environ
    if posix_support or win_support:
      return func(text)
    return text

  return wrapper


class CLI:
  def __init__(self, progname, verbosity=0):
    self.verbosity = verbosity
    self.footprint = CLI.bold(os.path.basename(progname)) + ':'

  @staticmethod
  @formatter
  def bold(text):
    return '{}{}{}'.format('\033[1m', text, '\033[0m')

  @staticmethod
  @formatter
  def red(text):
    return '{}{}{}'.format('\033[31m', text, '\033[0m')

  @staticmethod
  @formatter
  def green(text):
    return '{}{}{}'.format('\033[32m', text, '\033[0m')

  def choose(self, options, title='Choose one of the following:'):
    self.print(title)

    for i, o in enumerate(options):
      self.print('[{}] {}'.format(i, o.key))

    try:
      choice = int(input('> '))
      print('debug', options[choice].value)
      return options[choice].value
    except IndexError:
      self.print('No valid option chosen.', error=True)
      sys.exit(1)
    except KeyboardInterrupt:
      sys.exit()

  def choose_serial(self):
    devices = [Option('{0:20} {1:40}'.format(device[0],
              device[1]), device) for device in STLink.devices()]

    if not devices:
      self.print('Could not find any ST-Link devices.', error=True)
      sys.exit(1)

    if len(devices) > 1:
      serial_ = self.choose(devices)[1]
      return serial_
    return None

  def print(self, text, verbosity=0, success=False, error=False):
    if self.verbosity < verbosity:
      return

    if error:
      sys.stderr.write('{} {}\n'.format(self.footprint, CLI.bold(CLI.red(text))))
    elif success:
      print(self.footprint, CLI.bold(CLI.green(text)))
    else:
      print(self.footprint, text)

  def call(self, arglist, exit_on_error=True, success_message=None):
    kwargs = {}
    if self.verbosity < 1:
      kwargs = {'stdout': subprocess.DEVNULL, 'stderr': subprocess.DEVNULL}

    try:
      if subprocess.call(arglist, **kwargs):
        self.print('Failure while executing {}.\n'.format(arglist[0]), error=True)
        if exit_on_error:
          sys.exit(1)
      elif success_message is not None:
        self.print(success_message, success=True, verbosity=2)
    except FileNotFoundError:
      self.print('Command not found: {}.'.format(arglist[0]), error=True)
      self.print('Make sure you\'ve included all the necessary executables in your PATH.')
      self.print('See README.md for more information.')
      sys.exit(1)
    except KeyboardInterrupt:
      self.print('{} interrupted.'.format(arglist[0]), error=True)
      sys.exit(1)
