from configparser import ConfigParser
from configparser import ExtendedInterpolation

# Access the paths from the config file
config = ConfigParser(interpolation=ExtendedInterpolation())
config.read("./Config/config.ini")

MUSIC_BASEPATH = config.get('paths', 'music_basepath')
SOUNDFONT_PATH = config.get('paths', 'soundfont_path')

SCREEN_WIDTH = int(config.get('screen', 'width'))
SCREEN_HEIGHT = int(config.get('screen', 'height'))