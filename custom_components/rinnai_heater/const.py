from collections import namedtuple

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.number import NumberDeviceClass
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import Platform

DOMAIN = "rinnai_heater"

DEFAULT_SCAN_INTERVAL = 15

Sensor = namedtuple("Sensor", ["address", "name", "coeff", "unit", "platform", "device_class", "enabled", "icon", "options", "debug"])

STATUS = []
ERROR = []

SENSORS_BUS_ARRAY = [
    #      addr    name                               coeff    unit      platform                       device_class                       enabled  icon                         options                  debug
    Sensor(0,      "status",                          None,    None,     Platform.SENSOR,               None,                              True,    None,                        None,                    False),
    Sensor(1,      "error",                           None,    None,     Platform.SENSOR,               None,                              True,    None,                        None,                    False),
    Sensor(3,      "actuations",                      1,       None,     Platform.SENSOR,               None,                              True,    None,                        None,                    False),
    Sensor(4,      "burning",                         1,       "h",      Platform.SENSOR,               SensorDeviceClass.DURATION,        True,    None,                        None,                    False),
    Sensor(5,      "standby",                         1,       "h",      Platform.SENSOR,               SensorDeviceClass.DURATION,        True,    None,                        None,                    False),
    Sensor(6,      "fan_diagnostic",                  0.1,    None,     Platform.SENSOR,               None,                              True,    None,                        None,                    True ),
    Sensor(7,      "fan_speed",                       0.1,     "Hz",     Platform.SENSOR,               SensorDeviceClass.FREQUENCY,       True,    None,                        None,                    False),
    Sensor(8,      "pov_current",                     0.1,     "mA",     Platform.SENSOR,               SensorDeviceClass.CURRENT,         True,    None,                        None,                    False),
    Sensor(9,      "power",                           0.1,     "kcal/min",Platform.SENSOR,              SensorDeviceClass.ENERGY,          True,    None,                        None,                    False),
    Sensor(10,     "water_inlet_temperature",         0.01,    "°C",     Platform.SENSOR,               SensorDeviceClass.TEMPERATURE,     True,    None,                        None,                    False),
    Sensor(11,     "water_outlet_temperature",        0.01,    "°C",     Platform.SENSOR,               SensorDeviceClass.TEMPERATURE,     True,    None,                        None,                    False),
    Sensor(12,     "water_flow",                      0.01,    "L/min",  Platform.SENSOR,               SensorDeviceClass.VOLUME_FLOW_RATE,True,    None,                        None,                    False),
    Sensor(13,     "water_flow_start",                0.01,    "L/min",  Platform.SENSOR,               SensorDeviceClass.VOLUME_FLOW_RATE,True,    None,                        None,                    False),
    Sensor(14,     "water_flow_stop",                 0.01,    "L/min",  Platform.SENSOR,               SensorDeviceClass.VOLUME_FLOW_RATE,True,    None,                        None,                    False),
    Sensor(15,     "target_temperature",              0.01,    "°C",     Platform.SENSOR,               SensorDeviceClass.TEMPERATURE,     True,    None,                        None,                    False),
    Sensor(16,     "device_ip",                       None,    None,     Platform.SENSOR,               None,                              True,    None,                        None,                    True ),
    Sensor(17,     "device_ip_priority",              None,    None,     Platform.SENSOR,               None,                              True,    None,                        None,                    True ),
    Sensor(18,     "target_temperature_raw",          None,    None,     Platform.SENSOR,               None,                              True,    None,                        None,                    True ),
    Sensor(19,     "serial_number",                   None,    None,     Platform.SENSOR,               None,                              True,    None,                        None,                    True ),
    Sensor(20,     "uptime",                          None,    "s",      Platform.SENSOR,               SensorDeviceClass.DURATION,        True,    None,                        None,                    False),
    Sensor(25,     "mac_address",                     None,    None,     Platform.SENSOR,               None,                              True,    None,                        None,                    True ),
    Sensor(37,     "wifi_signal",                     None,    "dB",     Platform.SENSOR,               SensorDeviceClass.SIGNAL_STRENGTH, True,    None,                        None,                    True ),
]

# SENSORS_TELA_ARRAY = [
#     #      addr    name                              coeff    unit      platform                       device_class                       enabled  icon                         options                  debug
#     Sensor(15201, "ChargerWorkstate",                None,    None,     Platform.SENSOR,               SensorDeviceClass.ENUM,            True,    None,                        CHR_WORKSTATE_NO,        False),
#     Sensor(15202, "MpptState",                       None,    None,     Platform.SENSOR,               SensorDeviceClass.ENUM,            True,    "mdi:solar-power",           MPPT_STATE_NO,           False),
#     Sensor(15203, "ChargingState",                   None,    None,     Platform.SENSOR,               SensorDeviceClass.ENUM,            True,    None,                        CHARGING_STATE_NO,       False),
#     Sensor(15205, "PvVoltage",                       0.1,     "V",      Platform.SENSOR,               SensorDeviceClass.VOLTAGE,         True,    None,                        None,                    False),
#     Sensor(15206, "BatteryVoltage",                  0.1,     "V",      Platform.SENSOR,               SensorDeviceClass.VOLTAGE,         True,    None,                        None,                    False),
#     Sensor(15207, "ChargerCurrent",                  0.1,     "A",      Platform.SENSOR,               SensorDeviceClass.CURRENT,         True,    "mdi:current-dc",            None,                    False),
#     Sensor(15208, "ChargerPower",                    None,    "W",      Platform.SENSOR,               SensorDeviceClass.POWER,           True,    None,                        None,                    False),
#     Sensor(15209, "RadiatorTemperature",             None,    "°C",     Platform.SENSOR,               SensorDeviceClass.TEMPERATURE,     True,    None,                        None,                    False),
#     Sensor(15210, "ExternalTemperature",             None,    "°C",     Platform.SENSOR,               SensorDeviceClass.TEMPERATURE,     True,    None,                        None,                    False),
#     Sensor(15211, "BatteryRelay",                    None,    None,     Platform.BINARY_SENSOR,        BinarySensorDeviceClass.POWER,     False,   "mdi:electric-switch",       None,                    False),
#     Sensor(15212, "PvRelay",                         None,    None,     Platform.BINARY_SENSOR,        BinarySensorDeviceClass.POWER,     False,   "mdi:electric-switch",       None,                    False),
#     Sensor(15213, "ChargerErrorMessage",             None,    None,     Platform.SENSOR,               None,                              True,    "mdi:alert-circle-outline",  None,                    False),
#     Sensor(15214, "ChargerWarningMessage",           None,    None,     Platform.SENSOR,               None,                              True,    "mdi:alert-outline",         None,                    False),
#     Sensor(15215, "BattVolGrade",                    None,    "V",      Platform.SENSOR,               SensorDeviceClass.VOLTAGE,         False,   None,                        None,                    False),
#     Sensor(15216, "RatedCurrent",                    0.1,     "A",      Platform.SENSOR,               SensorDeviceClass.CURRENT,         False,   "mdi:current-dc",            None,                    False),
#     Sensor(15217, "AccumulatedPower",                None,    "kWh",    Platform.SENSOR,               SensorDeviceClass.ENERGY,          True,    None,                        None,                    False),
#     Sensor(15219, "AccumulatedTime",                 None,    "s",      Platform.SENSOR,               SensorDeviceClass.DURATION,        False,   "mdi:clock-outline",         None,                    False),
# ]
