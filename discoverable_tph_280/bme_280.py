import bme280
from smbus2 import SMBus


class BME_280:
    port: int = None
    address = None
    bus: SMBus = None
    temperature: float = None
    pressure: float = None
    humidity: float = None

    def __init__(cls, port: int = 1, address=0x76):
        cls.port = port
        cls.address = address
        cls.bus = SMBus(port)

    def sample(cls):
        data = bme280.sample(cls.bus, cls.address)
        cls.temperature = data.temperature
        cls.pressure = data.pressure
        cls.humidity = data.temperature

    def __str__(cls):
        return f"port: {cls.port}, address: {cls.address}"
