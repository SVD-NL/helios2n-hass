from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD

from py2n import Py2NDevice, Py2NConnectionData

from .const import DOMAIN, PLATFORMS

async def async_setup_entry(hass: HomeAssistant, config: ConfigType) -> bool:
	aiohttp_session = async_get_clientsession(hass)
	connection_data = Py2NConnectionData(host= config.data[CONF_HOST], username=config.data[CONF_USERNAME], password=config.data[CONF_PASSWORD])
	hass.data.setdefault(DOMAIN,{})[config.entry_id] = await Py2NDevice.create(aiohttp_session, connection_data)
	hass.async_create_task(
		hass.config_entries.async_forward_entry_setups(
		config, PLATFORMS
		)
	)
	return True
