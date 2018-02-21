"""
Sensor for monitoring the size of a file.
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.filesize/
"""
import datetime
import logging
import os

import voluptuous as vol

from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA

_LOGGER = logging.getLogger(__name__)

CONF_DIR_PATHS = 'dir_paths'
ICON = 'mdi:file-multiple'

#PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
#    vol.Required(CONF_DIR_PATHS):
#        vol.All(cv.ensure_list, [cv.isdir]),
#})

def get_number_files(path):
    num_files = len([f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))])
    return num_files
    
def del_old_files(path):
    for dirpath, dirnames, filenames in os.walk(path):
       for file in filenames:
          curpath = os.path.join(dirpath, file)
          file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(curpath))
          if datetime.datetime.now() - file_modified > datetime.timedelta(hours=24):
              os.remove(curpath)

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the file size sensor."""
    sensors = []
    for path in config.get(CONF_DIR_PATHS):
        if not hass.config.is_allowed_path(path):
            _LOGGER.error(
                "Filepath %s is not valid or allowed", path)
            return
        else:
            sensors.append(dir_files(path))

    if sensors:
        add_devices(sensors, True)


class dir_files(Entity):
    """Encapsulates file size information."""

    def __init__(self, path):
        """Initialize the data object."""
        self._path = path   # Need to check its a valid path
        self._size = None
        self._number_files = 0
        self._name = path
        self._unit_of_measurement = 'files'

    def update(self):
        """Update the sensor."""
        self._number_files = get_number_files(self._path)
        #self._last_updated = get_last_updated(self._path)

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the number of files."""
        state_nf = self._number_files
        return state_nf

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return ICON

    @property
    def device_state_attributes(self):
        """Return other details about the sensor state."""
        attr = {
            'path': self._path,
            'number_files': self._number_files,
            }
        return attr

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit_of_measurement