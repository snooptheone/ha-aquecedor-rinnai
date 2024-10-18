import logging
import re
from typing import Any

from homeassistant.components.button import ButtonEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    heater = hass.data[DOMAIN][entry.entry_id]
    entities = []

    inc = RinnaiHeaterIncButton(heater)
    entities.append(inc)

    dec = RinnaiHeaterDecButton(heater)
    entities.append(dec)

    async_add_entities(entities)
    return True


class RinnaiHeaterIncButton(ButtonEntity):
    def __init__(self, heater):
        self._heater = heater

        self._attr_has_entity_name = True
        self._attr_unique_id = "temperature_increase" + heater._serial_number
        self._attr_name = re.sub(
            r"(?<=[a-z])(?=[A-Z])", " ", "temperature_increase"
        ).capitalize()
        self._attr_icon = "mdi:thermometer-chevron-up"

    async def async_press(self):
        await self._heater.inc()

    @property
    def device_info(self) -> dict[str, Any] | None:
        return self._heater._device_info()

    @property
    def available(self) -> dict[str, Any] | None:
        return True


class RinnaiHeaterDecButton(ButtonEntity):
    def __init__(self, heater):
        self._heater = heater

        self._attr_has_entity_name = True
        self._attr_unique_id = "temperature_decrease" + heater._serial_number
        self._attr_name = re.sub(
            r"(?<=[a-z])(?=[A-Z])", " ", "temperature_decrease"
        ).capitalize()
        self._attr_icon = "mdi:thermometer-chevron-down"

    async def async_press(self):
        await self._heater.dec()

    @property
    def device_info(self) -> dict[str, Any] | None:
        return self._heater._device_info()

    @property
    def available(self) -> dict[str, Any] | None:
        return True
