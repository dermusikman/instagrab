# instagrab
Grab images and video from Instagram

usage: instagrab.py [-h] [-w S] [-nv] [-v] U

Grab images and video from an Instagram account.

positional arguments:
  U               Username of account from which to grab media

optional arguments:
  -h, --help      show this help message and exit
  -w S, --wait S  Random wait multiplier in seconds
  -nv, --novideo
  -v, --verbose

NB: Random wait is necessary to prevent Instagram from blocking us. It's also
polite.

