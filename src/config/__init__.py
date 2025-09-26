import os

import yaml
from sqlmodel import Field

from base_module import (
    ExternalPgConfig,
    BaseConfig,
    BaseServiceConfig,
)


class DeviceConfig(BaseConfig):
    """."""

    host: str = Field('127.0.0.1')
    port: int = Field(8003)


class DevicesConfig(BaseConfig):
    """."""

    plc: DeviceConfig = Field()
    scanner: DeviceConfig = Field()
    printer: DeviceConfig = Field()


class InstanceConfig(BaseConfig):
    """."""

    host: str = Field('0.0.0.0')
    port: int = Field(80)
    tcp_plc_port: int = Field(7500)
    tcp_scanner_port: int = Field(7501)
    api_str: str = Field('/api/v1')


class ServiceConfig(BaseServiceConfig):
    """."""

    pg: ExternalPgConfig = Field()
    devices: DevicesConfig = Field()
    log_level: int = Field(default=10)
    instance: InstanceConfig = Field()


config: ServiceConfig = ServiceConfig.load(
    yaml.safe_load(
        open(os.getenv('YAML_PATH', 'config.yaml'))
    ) or {})