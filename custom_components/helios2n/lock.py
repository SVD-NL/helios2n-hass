import logging

from typing import Any, Coroutine
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.lock import LockEntity

from py2n import Py2NDevice

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config: ConfigType, async_add_entities: AddEntitiesCallback):
    device: Py2NDevice = hass.data[DOMAIN][config.entry_id]
    entities = []
    for switch in device.data.switches:
        if switch.enabled and switch.mode == "bistable":
            entities.append(Helios2nLockEntity(device, switch.id))
    async_add_entities(entities)
    return True

class Helios2nLockEntity(LockEntity):
    _attr_has_entity_name = True
    _attr_should_poll = True

    def __init__(self, device: Py2NDevice, switch_id: int) -> None:
        self._device = device
        self._attr_unique_id = f"{self._device.data.serial}_switch_{switch_id}"
        self._attr_name = f"Switch {switch_id}"
        self._switch_id = switch_id

    async def async_update(self):
        await self._device.update_switch_status()

    @property
    def device_info(self) ->DeviceInfo:
        return DeviceInfo(
            id = self._device.data.serial,
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

    async def async_unlock(self) -> Coroutine[Any, Any, None]:
        await self._device.set_switch(self._switch_id, True)
        await self.async_update_ha_state(True)

    async def async_lock(self) -> Coroutine[Any, Any, None]:
        await self._device.set_switch(self._switch_id, False)
        await self.async_update_ha_state(True)
