import os
import sys
import subprocess

from serial.tools.list_ports import comports

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

  def choose_port(self):
    ports = comports()
    if ports:
      self.print('Choose one of the following ports:')
      for i, p in enumerate(ports):
        self.print('[{0}] {1:40} {2:20}'.format(i, p.device, p.description))
      try:
        choice = input('> ')
        port = ports[int(choice)].device
        return port
      except IndexError:
        self.print('No valid port chosen.', error='True')
        sys.exit(1)
      except KeyboardInterrupt:
        sys.exit()
    else:
      self.print('No COM ports available.', error=True)
      sys.exit(1)

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
