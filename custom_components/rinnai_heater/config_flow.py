"""Config flow for Rinnai Heater integration."""

import logging
from collections.abc import Mapping
from typing import Any

import voluptuous as vol
from homeassistant.core import callback
from homeassistant.helpers.schema_config_entry_flow import (
    SchemaConfigFlowHandler,
    SchemaFlowFormStep,
)

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required("name"): str,
        vol.Required("host"): str,
        vol.Required("scan_interval", default=DEFAULT_SCAN_INTERVAL): vol.Coerce(float),
    }
)

CONFIG_FLOW = {
    "user": SchemaFlowFormStep(schema=CONFIG_SCHEMA),
}

OPTIONS_FLOW = {
    "init": CONFIG_FLOW["user"],
    **CONFIG_FLOW,
}


class RinnaiHeaterConfigFlow(SchemaConfigFlowHandler, domain=DOMAIN):
    """Handle a config flow for Rinnai Heater."""

    config_flow = CONFIG_FLOW
    options_flow = OPTIONS_FLOW

    @callback
    def async_config_entry_title(self, options: Mapping[str, Any]) -> str:
        """Return config entry title."""
        _LOGGER.debug("async_config_entry_title: %s", options)
        return f"Rinnai Heater ({options['name']})"
