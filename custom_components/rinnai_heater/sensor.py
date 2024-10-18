"""This module contains the RinnaiHeaterSensor class and the setup function for the Rinnai heater sensors."""

import logging
import re

from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor.const import (
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, Platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import RinnaiHeater, RinnaiHeaterInfo
from .const import DOMAIN, SENSORS, Sensor

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    heater = hass.data[DOMAIN][entry.entry_id]
    entities = []

    for sensor_info in SENSORS:
        if sensor_info.platform == Platform.SENSOR:
            sensor = RinnaiHeaterSensor(heater, sensor_info)
            entities.append(sensor)

    async_add_entities(entities)
    return True


class RinnaiHeaterSensor(SensorEntity):
    """Representation of a Rinnai Heater Sensor."""

    def __init__(self, heater: RinnaiHeater, sensor_info: Sensor) -> None:
        """Initialize the sensor."""
        _LOGGER.debug("RinnaiHeaterSensor: %s, %s", sensor_info, heater)
        self._heater = heater
        self._key = sensor_info.name
        self._coeff = sensor_info.coeff

        self._attr_has_entity_name = True
        self._attr_unique_id = f"{heater.data["serial_number"]}_{self._key}"
        self._attr_name = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", self._key).capitalize()
        self._attr_native_unit_of_measurement = sensor_info.unit
        self._attr_device_class = (
            sensor_info.device_class
            if isinstance(sensor_info.device_class, SensorDeviceClass)
            else None
        )
        self._attr_entity_registry_enabled_default = sensor_info.enabled
        self._attr_icon = sensor_info.icon
        self._attr_options = sensor_info.options
        self._attr_entity_category = (
            EntityCategory.DIAGNOSTIC if sensor_info.debug else None
        )

        if self._coeff is not None:
            if self._attr_device_class in (
                SensorDeviceClass.WATER,
                SensorDeviceClass.ENERGY,
            ):
                self._attr_state_class = SensorStateClass.TOTAL_INCREASING
            else:
                self._attr_state_class = SensorStateClass.MEASUREMENT
            self._attr_suggested_display_precision = str(self._coeff).count("0")

    async def async_added_to_hass(self):
        self._heater.async_add_rinnai_heater_sensor(self._heater_data_updated)

    async def async_will_remove_from_hass(self) -> None:
        self._heater.async_remove_rinnai_heater_sensor(self._heater_data_updated)

    @callback
    def _heater_data_updated(self):
        self.async_write_ha_state()

    @property
    def state(self):
        if self._key in self._heater.data:
            if self._attr_options is not None:
                return self._attr_options[self._heater.data[self._key]]
            if self._coeff is None:
                return self._heater.data[self._key]
            return float(self._heater.data[self._key]) * self._coeff

    @property
    def device_info(self) -> RinnaiHeaterInfo:
        """Return device information."""
        return self._heater.device_info()

    @property
    def available(self) -> bool:
        """Return True if the sensor is available."""
        return self._key in self._heater.data
