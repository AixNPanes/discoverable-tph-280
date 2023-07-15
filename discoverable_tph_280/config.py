""" Configuration files """
from __future__ import annotations
from os.path import isfile, exists, dirname, abspath
from os import environ
from pydantic import BaseModel
from pydantic_yaml import YamlModel
from .util import logger


class MQTT(BaseModel):
    host: str = "hastings.attlocal.net"
    username: str = "homeassistant"
    password: str = ""
    discovery_prefix: str = "homeassistant"
    state_prefix: str = "hmd"


class GPIO(BaseModel):
    port: int = 1
    address: int = 0x76


class Config(YamlModel):
    mqtt_broker: MQTT = MQTT()
    gpio: GPIO = GPIO()

    @staticmethod
    def _readfile(filepath) -> Config:
        config_file = abspath(filepath)
        logger.debug(f"importing logfile from file: {config_file}")
        with open(config_file, "r", encoding="utf-8") as f:
            return Config.parse_raw(f.read(), proto="yaml")

    @staticmethod
    def _config(filepath: str = None, string: str = None) -> Config:
        config: Config = None
        if string:
            logger.debug("importing logfile from string")
            config = Config.parse_raw(string)
        elif filepath:
            if isfile(filepath) and exists(filepath):
                config = Config._readfile(filepath)
            raise FileNotFoundError(filepath)
        else:
            config_file = abspath(".config.yaml")
            if isfile(config_file) and exists(config_file):
                config = Config._readfile(config_file)
            else:
                config_file = abspath(dirname(__file__) + "/.config.yaml")
                if isfile(config_file) and exists(config_file):
                    config = Config._readfile(config_file)
                else:
                    config = Config()
        return config

    @staticmethod
    def config() -> Config:
        config_filepath: str = None
        if "config" in environ:
            config_filepath = environ["config"]
        return Config._config(filepath=config_filepath)


config = Config.config()
