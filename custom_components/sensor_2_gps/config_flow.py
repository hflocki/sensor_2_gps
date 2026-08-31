"""Config flow for Sensor 2 GPS Tracker integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
import homeassistant.helpers.config_validation as cv

DOMAIN = "sensor_2_gps"

CONF_NAME = "name"
CONF_LATITUDE_SENSOR = "latitude_sensor"
CONF_LONGITUDE_SENSOR = "longitude_sensor"
CONF_ALTITUDE_SENSOR = "altitude_sensor"
CONF_SPEED_SENSOR = "speed_sensor"

class Sensor2GpsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Sensor 2 GPS Tracker."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data=user_input
            )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default="Camper GPS"): str,
                vol.Required(CONF_LATITUDE_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
                vol.Required(CONF_LONGITUDE_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
                vol.Optional(CONF_ALTITUDE_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
                vol.Optional(CONF_SPEED_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
