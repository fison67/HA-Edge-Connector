"""Config flow for K-Weather."""
import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import (CONF_SCAN_INTERVAL)

from homeassistant.helpers.device_registry import (
    CONNECTION_UPNP,
    async_get as async_get_device_registry,
)


DOMAIN              = 'st_edge_connector'

MODEL               = 'Edge Driver'
CONNECTIONS_VALUE   = "fison67"
IDENTIFIERS_VALUE   = "fison67"
CONF_HUB_ADDR       = 'hub_addr'
CONF_HA_ADDR        = 'ha_addr'
CONF_HA_PORT        = 'ha_port'
CONF_DEVICE         = 'device'

_LOGGER = logging.getLogger(__name__)

class HAConnectorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HA-Connector."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    @staticmethod
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return DeviceOptionsFlowHandler(config_entry)


    def __init__(self):
        """Initialize flow."""
        self._hub_addr: Required[str] = None

    async def async_step_config(self, user_input=None):
        """Confirm the setup."""

        schema = vol.Schema(
            {
                vol.Required(
                   CONF_DEVICES,
                   default="all",
                ): vol.In(self.getAllDeviceNames(self.hass))
            }
        )

        return self.async_show_form(
            step_id="config", data_schema=schema, errors=errors or {}
        )


    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            self._hub_addr         = user_input[CONF_HUB_ADDR]
            self._ha_addr          = user_input[CONF_HA_ADDR]
            self._ha_port          = user_input[CONF_HA_PORT]
            return self.async_create_entry(title=DOMAIN, data=user_input)

        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is None:
            return self._show_user_form(errors)

    async def async_step_import(self, import_info):
        """Handle import from config file."""
        return await self.async_step_user(import_info)

    @callback
    def _show_user_form(self, errors=None):
        schema = vol.Schema(
            {
                vol.Required(CONF_HUB_ADDR, default=None): str,
                vol.Required(CONF_HA_ADDR, default='192.168.0.100'): str,
                vol.Required(CONF_HA_PORT, default=20000): int,
            }
        )
        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors or {}
        )



class DeviceOptionsFlowHandler(config_entries.OptionsFlow):

    def __init__(self, config_entry):
        self.config_entry = config_entry
        self.updated_config = {}
        self.accept = ["switch", "cover", "light", "binary_sensor"]

    def getAllDeviceNames(self, hass):
        list = hass.states.async_all()
        result = []
        for state in list:
            entity_id = state.entity_id
            entity_type = entity_id.split(".")[0]
            if (DOMAIN not in entity_id) and (entity_type in self.accept):
                result.append(state.name + " [" + state.entity_id + "]")
        return result

    async def async_step_init(self, user_input=None):
        return await self.async_step_basic_options()

    async def async_step_basic_options(self, user_input=None):
        schema = vol.Schema(
            {
                vol.Required(
                   CONF_DEVICE,
                   default="",
                ): vol.In(self.getAllDeviceNames(self.hass))
            }
        )

        return self.async_show_form(
            step_id="config", data_schema=schema, errors={}, last_step=True
        )

    async def async_step_config(self, user_input=None):

        if user_input is not None:
            selected = user_input.get(CONF_DEVICE, "").split("[")
            title = selected[1][0:len(selected[1])]

            device_registry = await self.hass.helpers.device_registry.async_get_registry()
            device = device_registry.async_get_device(
                connections={(CONNECTION_UPNP, CONNECTIONS_VALUE)},
                identifiers={(DOMAIN, IDENTIFIERS_VALUE)},
            )

            entity_registry = await self.hass.helpers.entity_registry.async_get_registry()
            entity = entity_registry.async_get_or_create(
                DOMAIN,
                "edge-driver",
                title,
                suggested_object_id=title,
                config_entry=self.config_entry,
                device_id=device.id,
            )

            return self.async_create_entry(title=selected, data=None)
