import logging
from typing import Any, Coroutine

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.switch import SwitchEntity
from homeassistant.const import Platform

from py2n import Py2NDevice

from .const import DOMAIN
from .coordinator import Helios2nPortDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)
PLATFORM = Platform.SWITCH

async def async_setup_entry(hass: HomeAssistant, config: ConfigType, async_add_entities: AddEntitiesCallback):
    device: Py2NDevice
    device: Py2NDevice = hass.data[DOMAIN][config.entry_id]
    coordinator: Helios2nPortDataUpdateCoordinator = hass.data[DOMAIN][PLATFORM]["coordinator"]
    entities = []
    for port in device.data.ports:
        if port.type == "output":
            entities.append(Helios2nPortSwitchEntity(coordinator, device, port.id))
    async_add_entities(entities)
    return True

class Helios2nPortSwitchEntity(CoordinatorEntity, SwitchEntity):
    _attr_has_entity_name = True
    _attr_entity_registry_enabled_default = False

    def __init__(self, coordinator: Helios2nPortDataUpdateCoordinator, device: Py2NDevice, port_id: str) -> None:
        super().__init__(coordinator)
        self._device = device
        self._attr_unique_id = f"{self._device.data.serial}_port_{port_id}"
        self._attr_name = port_id
        self._port_id = port_id

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers = {(DOMAIN, self._device.data.serial), (DOMAIN, self._device.data.mac)},
            name= self._device.data.name,
            manufacturer = "2n/Helios",
            model = self._device.data.model,
            hw_version = self._device.data.hardware,
            sw_version = self._device.data.firmware,
        )

    @property
    def is_on(self) -> bool:
        for port in self._device.data.ports:
            if port.id == self._port_id:
                return port.state

    async def async_turn_on(self, **kwargs) -> Coroutine[Any, Any, None]:
        await self._device.set_port(self._port_id, True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> Coroutine[Any, Any, None]:
        await self._device.set_port(self._port_id, False)
        await self.coordinator.async_request_refresh()
