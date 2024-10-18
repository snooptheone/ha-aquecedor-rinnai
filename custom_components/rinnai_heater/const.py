"""Constants and sensor definitions for the Rinnai Heater integration."""

from typing import NamedTuple

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.sensor.const import SensorDeviceClass
from homeassistant.const import Platform

DOMAIN = "rinnai_heater"

DEFAULT_SCAN_INTERVAL = 15

class Sensor(NamedTuple):
    """Represents a sensor with various attributes."""

    name: str
    coeff: float|None
    unit: str|None
    platform: Platform
    device_class: BinarySensorDeviceClass | SensorDeviceClass | None
    enabled: bool
    icon: str|None
    options: list[str]|None
    debug: bool|None


STATUS = []
ERROR = []

TEMPERATURES_MAP = {
    "3": 3500,
    "4": 3600,
    "5": 3700,
    "6": 3800,
    "7": 3900,
    "8": 4000,
    "9": 4100,
    "10": 4200,
    "11": 4300,
    "12": 4400,
    "13": 4500,
    "14": 4600,
    "16": 4800,
    "18": 5000,
    "19": 5500,
    "20": 6000,
}

SENSORS = [
    #      name                               coeff    unit         platform                       device_class                        enabled  icon                         options                  debug
    Sensor("status",                          1,       None,        Platform.SENSOR,               None,                               True,    None,                        None,                    False),
    Sensor("flame",                           None,    None,        Platform.BINARY_SENSOR,        BinarySensorDeviceClass.POWER,      True,    "mdi:fire",                  None,                    False),
    Sensor("error",                           1,       None,        Platform.SENSOR,               None,                               True,    "mdi:alert-circle",          None,                    False),
    Sensor("actuations",                      1,       None,        Platform.SENSOR,               None,                               True,    "mdi:shimmer",               None,                    False),
    Sensor("burning_hours",                   1,       "h",         Platform.SENSOR,               SensorDeviceClass.DURATION,         True,    "mdi:fire",                  None,                    False),
    Sensor("standby_hours",                   1,       "h",         Platform.SENSOR,               SensorDeviceClass.DURATION,         True,    "mdi:fire-off",              None,                    False),
    Sensor("fan_diagnostic",                  0.1,     None,        Platform.SENSOR,               None,                               False,   "mdi:fan",                   None,                    True ),
    Sensor("fan_speed",                       0.1,     "Hz",        Platform.SENSOR,               SensorDeviceClass.FREQUENCY,        True,    "mdi:fan",                   None,                    False),
    Sensor("pov_current",                     0.1,     "mA",        Platform.SENSOR,               SensorDeviceClass.CURRENT,          True,    "mdi:current-ac",            None,                    False),
    Sensor("power",                           0.01,    "kcal/min",  Platform.SENSOR,               SensorDeviceClass.POWER,            True,    "mdi:gas-burner",            None,                    False),
    Sensor("water_inlet_temperature",         0.01,    "°C",        Platform.SENSOR,               SensorDeviceClass.TEMPERATURE,      True,    "mdi:thermometer-water",     None,                    False),
    Sensor("water_outlet_temperature",        0.01,    "°C",        Platform.SENSOR,               SensorDeviceClass.TEMPERATURE,      True,    "mdi:thermometer-water",     None,                    False),
    Sensor("water_flow",                      0.01,    "L/min",     Platform.SENSOR,               SensorDeviceClass.VOLUME_FLOW_RATE, True,    "mdi:water",                 None,                    False),
    Sensor("water_flow_start",                0.01,    "L/min",     Platform.SENSOR,               SensorDeviceClass.VOLUME_FLOW_RATE, True,    "mdi:water-check",           None,                    False),
    Sensor("water_flow_stop",                 0.01,    "L/min",     Platform.SENSOR,               SensorDeviceClass.VOLUME_FLOW_RATE, True,    "mdi:water-off",             None,                    False),
    Sensor("target_temperature",              0.01,    "°C",        Platform.SENSOR,               SensorDeviceClass.TEMPERATURE,      True,    "mdi:water-thermometer",     None,                    False),
    Sensor("device_ip",                       None,    None,        Platform.SENSOR,               None,                               True,    "mdi:ip-network",            None,                    True ),
    Sensor("device_ip_priority",              None,    None,        Platform.SENSOR,               None,                               True,    "mdi:ip-network",            None,                    True ),
    Sensor("target_temperature_raw",          1,       None,        Platform.SENSOR,               None,                               False,   "mdi:water-thermometer",     None,                    True ),
    Sensor("serial_number",                   None,    None,        Platform.SENSOR,               None,                               False,   None,                        None,                    True ),
    Sensor("uptime",                          1,       "s",         Platform.SENSOR,               SensorDeviceClass.DURATION,         False,   None,                        None,                    False),
    Sensor("mac_address",                     None,    None,        Platform.SENSOR,               None,                               False,   "mdi:network",               None,                    True ),
    Sensor("wifi_signal",                     1,       "dB",        Platform.SENSOR,               SensorDeviceClass.SIGNAL_STRENGTH,  True,    None,                        None,                    True ),

    Sensor("water_usage",                     1,       "L",         Platform.SENSOR,               SensorDeviceClass.WATER,            True,    None,                        None,                    False),
    Sensor("gas_usage",                       1,       "kcal",      Platform.SENSOR,               SensorDeviceClass.ENERGY,           True,    "mdi:meter-gas",             None,                    False),
    Sensor("water_usage_last_week",           1,       "L",         Platform.SENSOR,               SensorDeviceClass.WATER,            True,    None,                        None,                    False),
    Sensor("gas_usage_last_week",             1,       "kcal",      Platform.SENSOR,               SensorDeviceClass.ENERGY,           True,    "mdi:meter-gas",             None,                    False),
]

SENSORS_BUS_ARRAY = {
    0: "status",
    1: "error",
    3: "actuations",
    4: "burning_hours",
    5: "standby_hours",
    6: "fan_diagnostic",
    7: "fan_speed",
    8: "pov_current",
    9: "power",
    10: "water_inlet_temperature",
    11: "water_outlet_temperature",
    12: "water_flow",
    13: "water_flow_start",
    14: "water_flow_stop",
    15: "target_temperature",
    16: "device_ip",
    17: "device_ip_priority",
    18: "target_temperature_raw",
    19: "serial_number",
    20: "uptime",
    25: "mac_address",
    37: "wifi_signal",
}

SENSORS_TELA_ARRAY = {
    0: "status",
    2: "flame",
    3: "burning_hours",
    4: "standby_hours",
    5: "water_flow",
    6: "device_ip_priority",
    7: "target_temperature_raw",
    8: "uptime",
}

SENSORS_CONSUMO_ARRAY = {
    1: "water_usage",
    2: "gas_usage",
    4: "water_usage_last_week",
    5: "gas_usage_last_week",
}
