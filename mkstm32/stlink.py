import sys
import serial

class STLink:
  def __init__(self, cli):
    self.cli = cli

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
