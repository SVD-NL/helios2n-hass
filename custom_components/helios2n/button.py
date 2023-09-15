import logging

from typing import Any, Coroutine
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.button import ButtonEntity, ButtonDeviceClass

from py2n import Py2NDevice

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config: ConfigType, async_add_entities: AddEntitiesCallback):
    device: Py2NDevice = hass.data[DOMAIN][config.entry_id]
    entities = []
    entities.append(Helios2nRestartButtonEntity(device))
    for switch in device.data.switches:
        if switch.enabled and switch.mode == "monostable":
            entities.append(Helios2nSwitchButtonEntity(device, switch.id))
    async_add_entities(entities)
    return True

class Helios2nSwitchButtonEntity(ButtonEntity):
    _attr_has_entity_name = True
    _attr_icon = "mdi:lock-clock"

    def __init__(self, device: Py2NDevice, switch_id: int) -> None:
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

    async def async_press(self) -> Coroutine[Any, Any, None]:
        await self._device.set_switch(self._switch_id, True)


class Helios2nRestartButtonEntity(ButtonEntity):
    _attr_has_entity_name = True
    _attr_device_class = ButtonDeviceClass.RESTART
    _attr_entity_registry_visible_default = False

    def __init__(self, device: Py2NDevice) -> None:
        self._device = device
        self._attr_unique_id = f"{self._device.data.serial}_restart"
        self._attr_name = "Restart"

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

    async def async_press(self):
        await self._device.restart()
