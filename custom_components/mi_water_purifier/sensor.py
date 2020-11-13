"""Support for Xiaomi water purifier C1."""

#'["run_status","f1_totaltime","f1_usedtime","f2_totaltime","f2_usedtime","tds_in","tds_out","rinse","temperature","tds_warn_thd","f3_totaltime","f3_usedtime"]'
import math
import logging

from homeassistant.const import (CONF_NAME, CONF_HOST, CONF_TOKEN, )
from homeassistant.helpers.entity import Entity
from homeassistant.exceptions import PlatformNotReady
from miio import Device, DeviceException

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['python-miio>=0.3.1']

TAP_WATER_QUALITY = {'name': 'Tap water', 'key': 'tds_in'}
FILTERED_WATER_QUALITY = {'name': 'Filtered water', 'key': 'tds_out'}
PP_COTTON_FILTER_REMAINING = {'name': 'PP cotton filter', 'key': 'pfd', 'days_key': 'pfp'}
RO_FILTER_REMAINING = {'name': 'RO filter', 'key': 'rfd', 'days_key': 'rfp'}
REAR_ACTIVE_CARBON_FILTER_REMAINING = {'name': 'Rear active carbon filter', 'key': 'rcfd', 'days_key': 'rcfp'}
TEMPERATURE = {'name': 'Water Temperature', 'key': 'temperature'}
RINSE = {'name': 'Rinse', 'key': 'rinse'}
TDS_WARN = {'name': 'TDS Warn', 'key': 'tds_warn_thd'}


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Perform the setup for Xiaomi water purifier."""

    host = config.get(CONF_HOST)
    name = config.get(CONF_NAME)
    token = config.get(CONF_TOKEN)

    _LOGGER.info("Initializing Xiaomi water purifier with host %s (token %s...)", host, token[:5])

    devices = []
    try:
        device = Device(host, token)
        waterPurifier = XiaomiWaterPurifier(device, name)
        devices.append(waterPurifier)
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, TAP_WATER_QUALITY))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, FILTERED_WATER_QUALITY))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, PP_COTTON_FILTER_REMAINING))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, RO_FILTER_REMAINING))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, REAR_ACTIVE_CARBON_FILTER_REMAINING))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, TEMPERATURE))
#        devices.append(XiaomiWaterPurifierSensor(waterPurifier, RINSE))
#        devices.append(XiaomiWaterPurifierSensor(waterPurifier, TDS_WARN))
    except DeviceException:
        _LOGGER.exception('Fail to setup Xiaomi water purifier')
        raise PlatformNotReady

    add_devices(devices)

class XiaomiWaterPurifierSensor(Entity):
    """Representation of a XiaomiWaterPurifierSensor."""

    def __init__(self, waterPurifier, data_key):
        """Initialize the XiaomiWaterPurifierSensor."""
        self._state = None
        self._data = None
        self._waterPurifier = waterPurifier
        self._data_key = data_key
        self.parse_data()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._data_key['name']

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        if self._data_key['key'] is TAP_WATER_QUALITY['key'] or \
           self._data_key['key'] is FILTERED_WATER_QUALITY['key']:
            return 'mdi:water'
        else:
            return 'mdi:filter-outline'

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        if self._data_key['key'] is TAP_WATER_QUALITY['key'] or \
           self._data_key['key'] is FILTERED_WATER_QUALITY['key']:
            return 'ppm'
        if self._data_key['key'] is TEMPERATURE['key']:
            return '°C'
        return '%'

    @property
    def device_state_attributes(self):
        """Return the state attributes of the last update."""
        attrs = {}

        if self._data_key['key'] is PP_COTTON_FILTER_REMAINING['key'] or \
           self._data_key['key'] is RO_FILTER_REMAINING['key'] or \
           self._data_key['key'] is REAR_ACTIVE_CARBON_FILTER_REMAINING['key']:
            attrs['days_resource'] = self._data[self._data_key['days_key']]

        return attrs

    def parse_data(self):
        if self._waterPurifier._data:
            self._data = self._waterPurifier._data
            self._state = self._data[self._data_key['key']]

    def update(self):
        """Get the latest data and updates the states."""
        self.parse_data()

class XiaomiWaterPurifier(Entity):
    """Representation of a XiaomiWaterPurifier."""

    def __init__(self, device, name):
        """Initialize the XiaomiWaterPurifier."""
        self._state = None
        self._device = device
        self._name = name
        self.parse_data()

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return 'mdi:water'

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return 'TDS'

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def hidden(self) -> bool:
        """Return True if the entity should be hidden from UIs."""
        return True

    @property
    def device_state_attributes(self):
        """Return the state attributes of the last update."""
        attrs = {}
        attrs[TAP_WATER_QUALITY['name']] = '{}TDS'.format(self._data[TAP_WATER_QUALITY['key']])
        attrs[PP_COTTON_FILTER_REMAINING['name']] = '{}%'.format(self._data[PP_COTTON_FILTER_REMAINING['key']])
        attrs[RO_FILTER_REMAINING['name']] = '{}%'.format(self._data[RO_FILTER_REMAINING['key']])
        attrs[REAR_ACTIVE_CARBON_FILTER_REMAINING['name']] = '{}%'.format(self._data[REAR_ACTIVE_CARBON_FILTER_REMAINING['key']])
        attrs[TEMPERATURE['name']] = '{} °C'.format(self._data[TEMPERATURE['key']])

        return attrs

    def parse_data(self):
        """Parse data."""
        try:
            data = {}
            data[TAP_WATER_QUALITY['key']] = self._device.send('get_prop', '["tds_in"]')[0]
            data[FILTERED_WATER_QUALITY['key']] = self._device.send('get_prop', '["tds_out"]')[0]
            data[TEMPERATURE['key']] = self._device.send('get_prop', '["temperature"]')[0]
            f1_totaltime = self._device.send('get_prop', '["f1_totaltime"]')[0] 
            f1_usedtime = self._device.send('get_prop', '["f1_usedtime"]')[0]
            f2_totaltime = self._device.send('get_prop', '["f2_totaltime"]')[0] 
            f2_usedtime = self._device.send('get_prop', '["f2_usedtime"]')[0]
            f3_totaltime = self._device.send('get_prop', '["f3_totaltime"]')[0] 
            f3_usedtime = self._device.send('get_prop', '["f3_usedtime"]')[0]

            pfd = int((f1_totaltime - f1_usedtime) / 24)
            data[PP_COTTON_FILTER_REMAINING['days_key']] = pfd
            data[PP_COTTON_FILTER_REMAINING['key']] = math.floor(pfd * 24 * 100 / f1_totaltime)
            rfd = int((f2_totaltime - f2_usedtime) / 24)
            data[RO_FILTER_REMAINING['days_key']] = rfd
            data[RO_FILTER_REMAINING['key']] = math.floor(rfd * 24 * 100 / f2_totaltime)
            rcfd = int((f3_totaltime - f3_usedtime) / 24)
            data[REAR_ACTIVE_CARBON_FILTER_REMAINING['days_key']] = rcfd
            data[REAR_ACTIVE_CARBON_FILTER_REMAINING['key']] = math.floor(rcfd * 24 * 100 / f3_totaltime)

            self._data = data
            self._state = self._data[FILTERED_WATER_QUALITY['key']]
        except DeviceException:
            _LOGGER.exception('Fail to get_prop from Xiaomi water purifier')
            self._data = None
            self._state = None
            raise PlatformNotReady

    def update(self):
        """Get the latest data and updates the states."""
        self.parse_data()
