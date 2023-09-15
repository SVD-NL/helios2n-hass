import logging

from typing import Any, Coroutine
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.lock import LockEntity
from homeassistant.const import Platform

from py2n import Py2NDevice

from .const import DOMAIN
from .coordinator import Helios2nSwitchDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)
PLATFORM = Platform.LOCK

async def async_setup_entry(hass: HomeAssistant, config: ConfigType, async_add_entities: AddEntitiesCallback):
    device: Py2NDevice = hass.data[DOMAIN][config.entry_id]
    coordinator: Helios2nSwitchDataUpdateCoordinator = hass.data[DOMAIN][PLATFORM]["coordinator"]
    entities = []
    for switch in device.data.switches:
        if switch.enabled and switch.mode == "bistable":
            entities.append(Helios2nLockEntity(coordinator, device, switch.id))
    async_add_entities(entities)
    return True

class Helios2nLockEntity(CoordinatorEntity, LockEntity):
    _attr_has_entity_name = True
    _attr_should_poll = True

    def __init__(self, coordinator: Helios2nSwitchDataUpdateCoordinator, device: Py2NDevice, switch_id: int) -> None:
        super().__init__(coordinator)
        self._device = device
        self._attr_unique_id = f"{self._device.data.serial}_switch_{switch_id}"
        self._attr_name = f"Switch {switch_id}"
        self._switch_id = switch_id

    @property
    def device_info(self) ->DeviceInfo:
        return DeviceInfo(
            identifiers = {(DOMAIN, self._device.data.serial), (DOMAIN, self._device.data.mac)},
            name= self._device.data.name,
            manufacturer = "2n/Helios",
            model = self._device.data.model,
            hw_version = self._device.data.hardware,
            sw_version = self._device.data.firmware,
        )

    @property
    def is_locked(self) -> bool:
        return not self._device.get_switch(self._switch_id)

    async def async_unlock(self, **kwargs) -> Coroutine[Any, Any, None]:
        await self._device.set_switch(self._switch_id, True)
        await self.coordinator.async_request_refresh()

    async def async_lock(self, **kwargs) -> Coroutine[Any, Any, None]:
        await self._device.set_switch(self._switch_id, False)
        await self.coordinator.async_request_refresh()
