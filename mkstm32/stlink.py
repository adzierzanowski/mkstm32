import re
import sys
import serial
import subprocess

class STLink:
  def __init__(self, cli):
    self.cli = cli

  # TODO: refactor this method
  def devices(self):
    devinfo = {}

    p = subprocess.Popen(['st-info', '--probe'], stdout=subprocess.PIPE)
    data = p.communicate()[0].decode('utf8').splitlines()

    # Get number of STLink devices
    n_regex = re.compile(r'\d+')
    n = int(re.findall(n_regex, data[0])[0])
    devinfo['count'] = n

    # Get names of the devices
    name_regex = re.compile(r'descr: (.+)')
    names = re.findall(name_regex, '\n'.join(data[1:]))

    # Get serial numbers
    serial_regex = re.compile(r'serial: (.+)')
    serials = re.findall(serial_regex, '\n'.join(data[1:]))

    devinfo['devices'] = list(zip(names, serials))
    
    return devinfo

  def probe(self):
    self.cli.call(['st-info', '--probe'])

  def reset(self):
    self.cli.call(['st-flash', 'reset'])

  def monitor(self, port):
    if port is None:
      port = self.cli.choose_port()

    s = None
    try:
      s = serial.Serial(port=port)
    except serial.serialutil.SerialException:
      self.cli.print('Serial port failure: {}'.format(port), error=True)

    if s is None:
      sys.exit(1)

    try:
      while True:
        try:
          sys.stdout.write(s.read().decode('utf8'))
        except UnicodeDecodeError:
          pass

    except KeyboardInterrupt:
      sys.exit()
