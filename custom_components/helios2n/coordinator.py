import logging
from datetime import timedelta
import async_timeout

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from py2n import Py2NDevice
from py2n.exceptions import DeviceApiError

_LOGGER = logging.getLogger(__name__)

class Helios2nPortDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, device: Py2NDevice):
        super().__init__(
            hass,
            _LOGGER,
            name="Helios2n Port Update",
            update_interval=timedelta(seconds=10)
        )
        self.device = device

    async def _async_update_data(self):
        try:
            async with async_timeout.timeout(10):
                await self.device.update_port_status()
        except DeviceApiError as err:
            raise UpdateFailed(f"Device API error: {err.error}") from err

class Helios2nSwitchDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, device: Py2NDevice):
        super().__init__(
            hass,
            _LOGGER,
            name="Helios2n Port Update",
            update_interval=timedelta(seconds=10)
        )
        self.device = device

    async def _async_update_data(self):
        try:
            async with async_timeout.timeout(10):
                await self.device.update_switch_status()
        except DeviceApiError as err:
            raise UpdateFailed(f"Device API error: {err.error}") from err
