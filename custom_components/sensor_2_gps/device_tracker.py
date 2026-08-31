"""Generisches Device Tracker Platform aus bestehenden Sensor-Entitaeten."""
import logging
from homeassistant.components.device_tracker import PLATFORM_SCHEMA, SourceType
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.const import CONF_NAME, STATE_UNKNOWN, STATE_UNAVAILABLE
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

_LOGGER = logging.getLogger(__name__)

CONF_LATITUDE_SENSOR = "latitude_sensor"
CONF_LONGITUDE_SENSOR = "longitude_sensor"
CONF_ALTITUDE_SENSOR = "altitude_sensor"
CONF_SPEED_SENSOR = "speed_sensor"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_LATITUDE_SENSOR): cv.entity_id,
        vol.Required(CONF_LONGITUDE_SENSOR): cv.entity_id,
        vol.Optional(CONF_ALTITUDE_SENSOR): cv.entity_id,
        vol.Optional(CONF_SPEED_SENSOR): cv.entity_id,
        vol.Optional(CONF_NAME, default="Sensor 2 GPS Tracker"): cv.string,
    }
)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the platform from yaml config."""
    async_add_entities([Sensor2GpsTracker(hass, config)], True)

class Sensor2GpsTracker(TrackerEntity):
    """Representation of a GPS Tracker built from individual sensors."""

    def __init__(self, hass, config):
        self.hass = hass
        self._attr_name = config[CONF_NAME]
        slug_name = config[CONF_NAME].lower().replace(" ", "_")
        self._attr_unique_id = f"sensor_2_gps_{slug_name}"
        
        self._lat_sensor = config[CONF_LATITUDE_SENSOR]
        self._lon_sensor = config[CONF_LONGITUDE_SENSOR]
        self._alt_sensor = config.get(CONF_ALTITUDE_SENSOR)
        self._speed_sensor = config.get(CONF_SPEED_SENSOR)

        self._latitude = None
        self._longitude = None
        self._altitude = None
        self._speed = None

    @property
    def source_type(self) -> SourceType:
        return SourceType.GPS

    @property
    def latitude(self) -> float | None:
        return self._latitude

    @property
    def longitude(self) -> float | None:
        return self._longitude

    @property
    def altitude(self) -> float | None:
        return self._altitude

    @property
    def extra_state_attributes(self):
        """Return extra attributes like speed."""
        attributes = {}
        if self._speed is not None:
            attributes["speed"] = self._speed
        return attributes

    async def async_update(self):
        """Fetch latest states from the specified sensors."""
        # Latitude & Longitude
        lat_state = self.hass.states.get(self._lat_sensor)
        lon_state = self.hass.states.get(self._lon_sensor)

        if lat_state and lon_state and lat_state.state not in (STATE_UNKNOWN, STATE_UNAVAILABLE):
            try:
                self._latitude = float(lat_state.state)
                self._longitude = float(lon_state.state)
            except ValueError:
                _LOGGER.warning("Could not convert lat/lon to float: %s, %s", lat_state.state, lon_state.state)

        # Altitude (optional)
        if self._alt_sensor:
            alt_state = self.hass.states.get(self._alt_sensor)
            if alt_state and alt_state.state not in (STATE_UNKNOWN, STATE_UNAVAILABLE):
                try:
                    self._altitude = float(alt_state.state)
                except ValueError:
                    pass

        # Speed (optional)
        if self._speed_sensor:
            speed_state = self.hass.states.get(self._speed_sensor)
            if speed_state and speed_state.state not in (STATE_UNKNOWN, STATE_UNAVAILABLE):
                try:
                    self._speed = float(speed_state.state)
                except ValueError:
                    pass
