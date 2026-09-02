"""Device tracker platform from sensors for Sensor 2 GPS Tracker."""
import logging
from homeassistant.components.device_tracker import SourceType, TrackerEntity
from homeassistant.const import STATE_UNKNOWN, STATE_UNAVAILABLE
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

CONF_NAME = "name"
CONF_LATITUDE_SENSOR = "latitude_sensor"
CONF_LONGITUDE_SENSOR = "longitude_sensor"
CONF_ALTITUDE_SENSOR = "altitude_sensor"
CONF_SPEED_SENSOR = "speed_sensor"
CONF_RAW_MODBUS = "raw_modbus"


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    """Set up the device tracker entity from config entry."""
    async_add_entities([Sensor2GpsTracker(hass, entry)], True)


class Sensor2GpsTracker(TrackerEntity):
    """Representation of a GPS Tracker built from individual sensors."""

    def __init__(self, hass: HomeAssistant, entry):
        self.hass = hass
        self._config = entry.data
        self._attr_name = self._config[CONF_NAME]
        self._attr_unique_id = f"sensor_2_gps_{entry.entry_id}"

        self._lat_sensor = self._config[CONF_LATITUDE_SENSOR]
        self._lon_sensor = self._config[CONF_LONGITUDE_SENSOR]
        self._alt_sensor = self._config.get(CONF_ALTITUDE_SENSOR)
        self._speed_sensor = self._config.get(CONF_SPEED_SENSOR)
        self._is_raw = self._config.get(CONF_RAW_MODBUS, False)

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

    def _parse_float(self, state_val: str | None) -> float | None:
        """Helper to clean degree symbols, commas and parse float safely."""
        if state_val is None:
            return None
        
        state_str = str(state_val).strip()
        if not state_str or state_str.lower() in (STATE_UNKNOWN, STATE_UNAVAILABLE, "none"):
            return None
            
        try:
            # Entfernt Grad-Symbole, Leerzeichen und ersetzt deutsche Kommas durch Punkte
            clean_str = state_str.replace("°", "").replace(",", ".").strip()
            return float(clean_str)
        except ValueError:
            return None

    async def async_update(self):
        """Fetch latest states from the specified sensors."""
        lat_state = self.hass.states.get(self._lat_sensor)
        lon_state = self.hass.states.get(self._lon_sensor)

        if lat_state and lon_state:
            raw_lat = self._parse_float(lat_state.state)
            raw_lon = self._parse_float(lon_state.state)

            if raw_lat is not None and raw_lon is not None and raw_lat != 0 and raw_lon != 0:
                if self._is_raw:
                    # Intelligente Skalierung: Nur teilen, wenn Wert > 180 (Modbus Integer)
                    self._latitude = raw_lat / 1000000.0 if abs(raw_lat) > 180 else raw_lat
                    self._longitude = raw_lon / 1000000.0 if abs(raw_lon) > 180 else raw_lon
                else:
                    self._latitude = raw_lat
                    self._longitude = raw_lon

        if self._alt_sensor:
            alt_state = self.hass.states.get(self._alt_sensor)
            if alt_state:
                alt_val = self._parse_float(alt_state.state)
                if alt_val is not None:
                    self._altitude = alt_val

        if self._speed_sensor:
            speed_state = self.hass.states.get(self._speed_sensor)
            if speed_state:
                speed_val = self._parse_float(speed_state.state)
                if speed_val is not None:
                    self._speed = speed_val
