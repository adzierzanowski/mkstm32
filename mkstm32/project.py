import os
import sys
import time
import shutil
import subprocess

class Project:
  standard_makefile = 'Makefile'
  cpp_makefile = 'Makefile_cpp.mk'

  def __init__(self, dir_, cli, stlink, cpp=False):
    self.cli = cli
    self.stlink = stlink
    self.start = None
    self.dir = os.path.abspath(dir_)
    self.cpp = cpp
    self.build_dir = 'build'

    self.bin = self.path(os.path.join(self.build_dir, self.name() + '.bin'))
    self.elf = self.path(os.path.join(self.build_dir, self.name() + '.elf'))
    self.hex = self.path(os.path.join(self.build_dir, self.name() + '.hex'))

    os.chdir(self.dir)

  def __enter__(self):
    self.start = time.time()
    return self

  def __exit__(self, ex_type, ex_val, traceback):
    took = time.time() - self.start
    if took > 0.01:
      self.cli.print('Done in {0:0.2f} seconds.'.format(time.time() - self.start), verbosity=2)

  def path(self, file_=''):
    return os.path.join(self.dir, file_)

  def name(self):
    return os.path.basename(self.dir)

  def compile(self):
    success_msg = 'Successfuly compiled firmware'
    if self.cpp:
      self.cli.print('Compiling for C++', verbosity=1)
      self.generate_cpp_makefile()
      self.cli.call(['make', '-f', self.path(Project.cpp_makefile)],
        success_message=success_msg)
    else:
      self.cli.print('Compiling for C', verbosity=1)
      self.cli.call(['make', '-f', self.path(Project.standard_makefile)],
        success_message=success_msg)

  def generate_cpp_makefile(self):
    with open(self.path(Project.standard_makefile), 'r') as f:
      data = f.read()

    data = data.replace('gcc', 'g++')
    splitdata = data.splitlines()

    for i, line in enumerate(splitdata):
      if 'LDFLAGS =' in line:
        splitdata.insert(i+1, 'LDFLAGS += -specs=nosys.specs')

      if 'CFLAGS =' in line:
        splitdata.insert(i+1, 'CFLAGS += -std=c++14')

    with open(self.path(Project.cpp_makefile), 'w') as f:
      f.write('\n'.join(splitdata))

  # TODO: refactor this method
  def upload(self):
    devices = self.stlink.devices()

    if devices['count'] > 1:
      self.cli.print('Choose one of the following devices')
      for i, p in enumerate(devices['devices']):
        self.cli.print('[{0}] {1:20} {2:40}'.format(i, p[0], p[1]))
      try:
        choice = input('> ')
        serial = devices['devices'][int(choice)][1]
        self.cli.call(['st-flash', '--serial', serial, 'write', self.bin, '0x8000000'],
          success_message='Successfully uploaded firmware.')

      except IndexError:
        self.cli.print('No valid device chosen.', error='True')
        sys.exit(1)
      except KeyboardInterrupt:
        sys.exit()

    else:
      self.cli.call(['st-flash', 'write', self.bin, '0x8000000'],
        success_message='Successfully uploaded firmware.')

  def debug(self):
    self.cli.print('Starting GDB server.', verbosity=1)

    kwargs = {}
    if self.cli.verbosity < 3:
      kwargs = {'stdout': subprocess.DEVNULL, 'stderr': subprocess.DEVNULL}

    gdb_server = subprocess.Popen(['st-util'], **kwargs)

    time.sleep(0.1)
    if gdb_server.poll():
      self.cli.print('Failed to start GDB server.', error=True)
    else:
      self.cli.print('Successfully started GDB server.', verbosity=2)

    try:
      self.cli.call(['arm-none-eabi-gdb', self.elf, '-ex', 'tar extended-remote :4242'])
    except KeyboardInterrupt:
      pass
    finally:
      self.cli.print('Closing GDB server.', verbosity=1)
      gdb_server.kill()
      self.cli.print('GDB server killed.', verbosity=2)

  def size(self):
    for file_ in [self.bin, self.elf, self.hex]:
      with open(file_, 'r') as f:
        f.seek(0, 2)
        self.cli.print('{}: {} B'.format(os.path.basename(file_), f.tell()))

  def clean(self):
    self.cli.print('Cleaning build directory.', verbosity=1)

    try:
      shutil.rmtree(self.build_dir)
      self.cli.print('Successfully cleaned build directory.', verbosity=2, success=True)
    except FileNotFoundError:
      self.cli.print('Build directory doesn\'t exist.', error=True)
