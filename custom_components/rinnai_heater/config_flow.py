import logging
from collections.abc import Mapping

import voluptuous as vol
from typing import Any
from homeassistant.core import callback
from homeassistant.helpers.schema_config_entry_flow import (
    SchemaConfigFlowHandler,
    SchemaFlowFormStep,
)

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({
    vol.Required("name"): str,
    vol.Required("host"): str,
    vol.Required("scan_interval", default=DEFAULT_SCAN_INTERVAL): vol.Coerce(float),
})

CONFIG_FLOW = {
    "user": SchemaFlowFormStep(schema=CONFIG_SCHEMA),
}

OPTIONS_FLOW = {
    "init": CONFIG_FLOW["user"],
    **CONFIG_FLOW,
}


class RinnaiHeaterConfigFlow(SchemaConfigFlowHandler, domain=DOMAIN):
    config_flow = CONFIG_FLOW
    options_flow = OPTIONS_FLOW

    # _LOGGER.debug("RinnaiHeaterConfigFlow")

    @callback
    def async_config_entry_title(self, options: Mapping[str, Any]) -> str:
        """Return config entry title."""
        _LOGGER.debug("async_config_entry_title: %s", options)
        msg = f"Rinnai Heater ({options['name']})"
        return msg
