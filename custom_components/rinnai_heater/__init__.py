"""Module provides the integration for the Rinnai Heater component in Home Assistant."""

import asyncio
import logging
from datetime import date, timedelta
from typing import NamedTuple

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_time_interval

from .const import (
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    SENSORS_BUS_ARRAY,
    SENSORS_CONSUMO_ARRAY,
    SENSORS_TELA_ARRAY,
)

PLATFORMS = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.WATER_HEATER,
]
_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Rinnai Heater component."""
    _LOGGER.debug("async_setup: %s", config)
    hass.data[DOMAIN] = {}
    # Return boolean to indicate that initialization was successful.
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool | None:
    """Set up a config entry for the Rinnai Heater component."""
    try:
        entry.async_on_unload(entry.add_update_listener(async_reload_entry))

        heater = RinnaiHeater(hass, entry)

        success_reading = await heater.bus()
        if not success_reading:
            raise ConfigEntryNotReady("Unable to fetch Rinnai device")
        # call async_set_unique_id(heater._serial_number) to set unique_id
        hass.config_entries.async_update_entry(
            entry, unique_id=heater.data["serial_number"]
        )
        hass.data[DOMAIN][entry.entry_id] = heater
        _LOGGER.debug("entry: %s", entry)

        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

        return True
    except ConfigEntryNotReady as ex:
        raise ex
    except Exception as ex:
        _LOGGER.exception("Error setting up device", exc_info=True)
        raise ConfigEntryNotReady("Unknown error connecting to device") from ex


async def async_unload_entry(hass, entry) -> bool:
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )

    if not unload_ok:
        return False

    hass.data[DOMAIN][entry.entry_id] = None
    return True


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update listener, called when the config entry options are changed."""
    await hass.config_entries.async_reload(entry.entry_id)


class RinnaiHeaterInfo(NamedTuple):
    """Class representing the device info for Rinnai Heater device."""

    connections: set[tuple[str, str]] | None
    identifiers: set[tuple[str, str]] | None
    name: str | None
    model: str | None
    manufacturer: str | None
    serial_number: str | None


class RinnaiHeater:
    """Class representing the Rinnai Heater device."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the Rinnai Heater device."""
        self._hass = hass
        self._client = async_get_clientsession(hass, verify_ssl=False)
        self._host = entry.options["host"]
        self._lock = asyncio.Lock()
        self._scan_interval = timedelta(
            seconds=entry.options.get("scan_interval", DEFAULT_SCAN_INTERVAL)
        )
        self._sensors = []
        self._reading = False
        self._name = entry.options["name"]

        self.data: dict[str, str] = {}
        # self._mac_address: str = None
        # self._serial_number: str = None

    @callback
    def async_add_rinnai_heater_sensor(self, update_callback) -> None:
        """Add a Rinnai heater sensor and set up the interval if it's the first sensor."""
        # This is the first sensor, set up interval.
        if not self._sensors:
            self._unsub_interval_method = async_track_time_interval(
                self._hass, self._async_refresh_data, self._scan_interval
            )

        self._sensors.append(update_callback)

    @callback
    async def async_remove_rinnai_heater_sensor(self, update_callback) -> None:
        self._sensors.remove(update_callback)

        if not self._sensors:
            """stop the interval timer upon removal of last sensor"""
            if self._unsub_interval_method:
                self._unsub_interval_method()
            self._unsub_interval_method = None
            await self.close()

    async def _async_refresh_data(self, _time: date | None = None) -> None:
        try:
            await self.bus()
            await self.consumo()
            await self.tela()

        except Exception:
            _LOGGER.exception("Error reading heater data")

    async def close(self) -> None:
        """Close the HTTP client session."""
        _LOGGER.info("closing http client")
        await self._client.close()

    async def request(self, endpoint: str) -> list[str]:
        """Send a request to the specified endpoint and return the response as a list of strings.

        Args:
            endpoint (str): The endpoint to request data from.

        Returns:
            list[str]: The response data as a list of strings, or empty if an error occurred.

        """

        _LOGGER.debug("requesting /%s", endpoint)

        async with self._lock:
            try:
                res = await self._client.get(f"http://{self._host}/{endpoint}")
                read = await res.text()
                _LOGGER.debug("response: %s", read)
                return read.split(",")
            except Exception:
                _LOGGER.exception("Error fetching /%s data", endpoint)
                self.data = {}  # clear data on error so entities become unavailable
                return []
            finally:
                self._reading = False

    async def inc(self) -> bool:
        """Increase the heater setting and update the data.

        Returns:
            bool: True if the data was successfully updated, False otherwise.

        """
        return self.update_data(await self.request("inc"), SENSORS_TELA_ARRAY)

    async def dec(self) -> bool:
        """Decrease the heater setting and update the data.

        Returns:
            bool: True if the data was successfully updated, False otherwise.

        """
        return self.update_data(await self.request("dec"), SENSORS_TELA_ARRAY)

    async def lig(self) -> bool:
        """Turn on the heater and update the data.

        Returns:
            bool: True if the data was successfully updated, False otherwise.

        """
        return self.update_data(await self.request("lig"), SENSORS_TELA_ARRAY)

    async def bus(self) -> bool:
        """Fetch and update the bus data from the heater.

        Returns:
            bool: True if the data was successfully updated, False otherwise.

        """
        return self.update_data(await self.request("bus"), SENSORS_BUS_ARRAY)

    async def tela(self) -> bool:
        """Fetch and update the tela data from the heater.

        Returns:
            bool: True if the data was successfully updated, False otherwise.

        """
        return self.update_data(await self.request("tela_"), SENSORS_TELA_ARRAY)

    async def consumo(self) -> bool:
        """Fetch and update the consumo data from the heater.

        Returns:
            bool: True if the data was successfully updated, False otherwise.

        """
        return self.update_data(await self.request("consumo"), SENSORS_CONSUMO_ARRAY)

    def update_data(
        self,
        response: list[str],
        sensors: dict[int, str],
        *,
        update_entities: bool = True,
    ) -> bool:
        """Update the data for the sensors and optionally update entities.

        Args:
            response (list[str]): The response data from the heater.
            sensors (dict[int, str]): The mapping of sensor addresses to names.
            update_entities (bool): Whether to update the entities with the new data. Defaults to True.

        Returns:
            bool: True if the data was successfully updated, False otherwise.

        """
        if response is None:
            return False

        for address, name in sensors.items():
            self.data[name] = response[address]

        if update_entities:
            for update_callback in self._sensors:
                update_callback()

        return True

    def device_info(self) -> RinnaiHeaterInfo:
        """Return the device information for the Rinnai Heater."""
        return RinnaiHeaterInfo(
            connections={(dr.CONNECTION_NETWORK_MAC, self.data["mac_address"])},
            identifiers={(DOMAIN, self.data["serial_number"])},
            name=self._name,
            model=self.data["model"],
            manufacturer="Rinnai",
            serial_number=self.data["serial_number"],
        )
