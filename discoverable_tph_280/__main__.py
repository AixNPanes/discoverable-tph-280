import time
import calendar
from .util import logger

from discoverable_tph_280.config import config

from .bme_280 import BME_280
from .thermometer import Thermometer
from .barometer import Barometer
from .hygrometer import Hygrometer

from ha_mqtt_discoverable import Settings


def main():
    bme_280 = BME_280(port=config.gpio.port, address=config.gpio.address)
    mqtt_settings = Settings.MQTT(
        host=config.mqtt_broker.host,
        username=config.mqtt_broker.username,
        password=config.mqtt_broker.password,
        discovery_prefix=config.mqtt_broker.discovery_prefix,
        state_prefix=config.mqtt_broker.state_prefix,
    )

    thermometer = Thermometer(mqtt=mqtt_settings, name="My Thermometer")
    barometer = Barometer(mqtt=mqtt_settings, name="My Barometer")
    hygrometer = Hygrometer(mqtt=mqtt_settings, name="My Hygrometer")

    thermometer.set_value(thermometer._entity.value)
    barometer.set_value(barometer._entity.value)
    hygrometer.set_value(hygrometer._entity.value)

    old_time = calendar.timegm(time.gmtime()) - 600
    logger.debug("loop")
    while True:
        bme_280.sample()

        new_time = calendar.timegm(time.gmtime())
        temp_change = bme_280.temperature - thermometer._entity.value
        pres_change = bme_280.pressure - barometer._entity.value
        hum_change = bme_280.humidity - hygrometer._entity.value
        time_change = old_time + 600 - new_time
        if (
            temp_change != 0
            or pres_change != 0
            or hum_change != 0
            or time_change != 0
        ):
            old_time = new_time
            thermometer.set_value(bme_280.temperature)
            barometer.set_value(bme_280.pressure)
            hygrometer.set_value(bme_280.humidity)
        time.sleep(10)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopping ...")
