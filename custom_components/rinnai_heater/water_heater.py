"""RinnaiHeaterWaterHeater class which integrates with the Home Assistant water heater component."""

import asyncio
import logging
import re
from typing import Any

from homeassistant.components.water_heater import (
    STATE_GAS,
    WaterHeaterEntity,
    WaterHeaterEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PRECISION_WHOLE, STATE_OFF, UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import RinnaiHeater, RinnaiHeaterInfo
from .const import DOMAIN, TEMPERATURES_MAP

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> bool:
    """Set up the Rinnai heater water heater entity."""
    heater = hass.data[DOMAIN][entry.entry_id]
    entities = []

    sensor = RinnaiHeaterWaterHeater(heater)
    entities.append(sensor)

    async_add_entities(entities)
    return True


class RinnaiHeaterWaterHeater(WaterHeaterEntity):
    """Representation of a Rinnai Heater Water Heater."""

    _attr_has_entity_name = True

    def __init__(self, heater: RinnaiHeater) -> None:
        """Initialize the RinnaiHeaterWaterHeater."""
        self._heater = heater

        self._attr_has_entity_name = True
        self._attr_unique_id = (
            f"{heater.data["serial_number"]}_{heater.data["mac_address"]}"
        )
        self._attr_name = re.sub(
            r"(?<=[a-z])(?=[A-Z])", " ", self._attr_unique_id
        ).capitalize()

        self._attr_min_temp = 35
        self._attr_max_temp = 60
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_operation_list = [STATE_GAS, STATE_OFF]
        self._attr_precision = PRECISION_WHOLE
        self._attr_supported_features = (
            WaterHeaterEntityFeature.OPERATION_MODE
            | WaterHeaterEntityFeature.TARGET_TEMPERATURE
        )

    @property
    def precision(self) -> float:
        """Return the precision of the system."""
        if hasattr(self, "_attr_precision"):
            return self._attr_precision
        return PRECISION_WHOLE

    async def async_added_to_hass(self) -> None:
        """Handle the entity being added to Home Assistant."""
        self._heater.async_add_rinnai_heater_sensor(self._heater_data_updated)

    async def async_will_remove_from_hass(self) -> None:
        """Handle the entity being removed from Home Assistant."""
        await self._heater.async_remove_rinnai_heater_sensor(self._heater_data_updated)

    @callback
    def _heater_data_updated(self) -> None:
        self.schedule_update_ha_state()

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature of the water heater."""
        if "water_outlet_temperature" in self._heater.data:
            return float(self._heater.data["water_outlet_temperature"]) * 0.01
        return None

    @property
    def target_temperature(self) -> float | None:
        """Return the target temperature of the water heater."""
        if "target_temperature_raw" in self._heater.data:
            return TEMPERATURES_MAP[self._heater.data["target_temperature_raw"]] * 0.01
        return None

    @property
    def is_on(self) -> bool:
        """Return True if the water heater is on, False otherwise."""
        return self._heater.data["status"] != "11"

    @property
    def current_operation(self) -> str:
        """Return the current operation mode of the water heater."""
        return STATE_GAS if self.is_on else STATE_OFF

    def set_temperature(self, **kwargs: Any) -> None:
        """Set the target temperature of the water heater."""

        _LOGGER.debug("async_set_temperature: %s", kwargs)

        temperature = kwargs.get("temperature")
        if temperature is None:
            _LOGGER.error("Temperature not provided in kwargs")
            return
        temperature *= 100

        nearest_temperature = min(
            TEMPERATURES_MAP.values(), key=lambda x: abs(x - temperature)
        )
        nearest_temperature_index = list(TEMPERATURES_MAP.values()).index(
            nearest_temperature
        )

        if self.target_temperature is not None:
            current_temperature = int(self.target_temperature * 100)
        else:
            _LOGGER.error("Target temperature is None")
            return
        current_temperature_index = list(TEMPERATURES_MAP.values()).index(
            current_temperature
        )

        steps = nearest_temperature_index - current_temperature_index

        _LOGGER.debug(
            "async_set_temperature: %s -> %s/%s - %s/%s - %s",
            temperature,
            nearest_temperature,
            nearest_temperature_index,
            current_temperature,
            current_temperature_index,
            steps,
        )

        for _i in range(abs(steps)):
            if steps > 0:
                asyncio.run(self._heater.inc())
            else:
                asyncio.run(self._heater.dec())

    async def async_set_operation_mode(self, mode) -> None:
        """Set the operation mode of the water heater."""
        if mode == STATE_GAS:
            await self.async_turn_on()
        elif mode == STATE_OFF:
            await self.async_turn_off()

    async def async_turn_on(self) -> None:
        """Turn on the water heater."""
        if not self.is_on:
            await self._heater.lig()

    async def async_turn_off(self) -> None:
        """Turn off the water heater."""
        if self.is_on:
            await self._heater.lig()

    @property
    def device_info(self) -> RinnaiHeaterInfo:
        """Return device information."""
        return self._heater.device_info()

    @property
    def available(self) -> bool:
        """Return True if the water heater is available."""
        return True
