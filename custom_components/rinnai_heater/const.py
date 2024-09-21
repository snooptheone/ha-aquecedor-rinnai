from collections import namedtuple

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.const import Platform

DOMAIN = "rinnai_heater"

DEFAULT_SCAN_INTERVAL = 15

Sensor = namedtuple("Sensor", ["name", "coeff", "unit", "platform", "device_class", "enabled", "icon", "options", "debug"])

STATUS = []
ERROR = []

SENSORS = [
    #      name                               coeff    unit         platform                       device_class                        enabled  icon                         options                  debug
    Sensor("status",                          None,    None,        Platform.SENSOR,               None,                               True,    None,                        None,                    False),
    Sensor("flame",                           None,    None,        Platform.BINARY_SENSOR,        BinarySensorDeviceClass.POWER,      True,    "mdi:fire",                  None,                    False),
    Sensor("error",                           None,    None,        Platform.SENSOR,               None,                               True,    "mdi:alert-circle",          None,                    False),
    Sensor("actuations",                      1,       None,        Platform.SENSOR,               None,                               True,    "mdi:shimmer",               None,                    False),
    Sensor("burning_hours",                   1,       "h",         Platform.SENSOR,               SensorDeviceClass.DURATION,         True,    "mdi:fire",                  None,                    False),
    Sensor("standby_hours",                   1,       "h",         Platform.SENSOR,               SensorDeviceClass.DURATION,         True,    "mdi:fire-off",              None,                    False),
    Sensor("fan_diagnostic",                  0.1,     None,        Platform.SENSOR,               None,                               True,    "mdi:fan",                   None,                    True ),
    Sensor("fan_speed",                       0.1,     "Hz",        Platform.SENSOR,               SensorDeviceClass.FREQUENCY,        True,    "mdi:fan",                   None,                    False),
    Sensor("pov_current",                     0.1,     "mA",        Platform.SENSOR,               SensorDeviceClass.CURRENT,          True,    "mdi:current-ac",            None,                    False),
    Sensor("power",                           0.01,    "kcal/min",  Platform.SENSOR,               SensorDeviceClass.ENERGY,           True,    "mdi:gas-burner",            None,                    False),
    Sensor("water_inlet_temperature",         0.01,    "°C",        Platform.SENSOR,               SensorDeviceClass.TEMPERATURE,      True,    "mdi:thermometer-water",     None,                    False),
    Sensor("water_outlet_temperature",        0.01,    "°C",        Platform.SENSOR,               SensorDeviceClass.TEMPERATURE,      True,    "mdi:thermometer-water",     None,                    False),
    Sensor("water_flow",                      0.01,    "L/min",     Platform.SENSOR,               SensorDeviceClass.VOLUME_FLOW_RATE, True,    "mdi:water",                 None,                    False),
    Sensor("water_flow_start",                0.01,    "L/min",     Platform.SENSOR,               SensorDeviceClass.VOLUME_FLOW_RATE, True,    "mdi:water-check",           None,                    False),
    Sensor("water_flow_stop",                 0.01,    "L/min",     Platform.SENSOR,               SensorDeviceClass.VOLUME_FLOW_RATE, True,    "mdi:water-off",             None,                    False),
    Sensor("target_temperature",              0.01,    "°C",        Platform.SENSOR,               SensorDeviceClass.TEMPERATURE,      True,    "mdi:water-thermometer",     None,                    False),
    Sensor("device_ip",                       None,    None,        Platform.SENSOR,               None,                               True,    "mdi:ip-network",            None,                    True ),
    Sensor("device_ip_priority",              None,    None,        Platform.SENSOR,               None,                               True,    "mdi:ip-network",            None,                    True ),
    Sensor("target_temperature_raw",          None,    None,        Platform.SENSOR,               None,                               True,    "mdi:water-thermometer",     None,                    True ),
    Sensor("serial_number",                   None,    None,        Platform.SENSOR,               None,                               True,    None,                        None,                    True ),
    Sensor("uptime",                          None,    "s",         Platform.SENSOR,               SensorDeviceClass.DURATION,         True,    None,                        None,                    False),
    Sensor("mac_address",                     None,    None,        Platform.SENSOR,               None,                               True,    "mdi:network",               None,                    True ),
    Sensor("wifi_signal",                     None,    "dB",        Platform.SENSOR,               SensorDeviceClass.SIGNAL_STRENGTH,  True,    None,                        None,                    True ),
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
