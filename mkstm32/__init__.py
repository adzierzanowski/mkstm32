from .version import __version__

if __name__ != 'setup.py':
  from .cli import *
  from .project import *
  from .stlink import *

