from typing import Any, Coroutine
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
import homeassistant.helpers.config_validation as cv
import aiohttp
import voluptuous as vol
from py2n import Py2NDevice, Py2NConnectionData
from py2n.exceptions import DeviceApiError
from .const import DOMAIN

class Helios2nConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
	"""Helios/2n config flow"""
	VERSION=1
	async def async_step_user(self, user_input: dict[str, Any] | None = None) -> Coroutine[Any, Any, config_entries.FlowResult]:
		errors = {}
		if user_input is not None:
			connect_options = Py2NConnectionData(user_input[CONF_HOST], user_input[CONF_USERNAME], user_input[CONF_PASSWORD])
			try:
				async with aiohttp.ClientSession() as session:
					device = await Py2NDevice.create(session, connect_options)
			except TimeoutError:
				errors["base"] = "timeout_error"
			except DeviceApiError:
				errors["base"] = "api_error"
			
			await self.async_set_unique_id(device.data.serial)
			self._abort_if_unique_id_configured()

			return self.async_create_entry(
				title=device.data.name,
				data=user_input
			)


		return self.async_show_form(
            step_id="user", data_schema=vol.Schema({
		    vol.Required(CONF_HOST): cv.string,
		    vol.Required(CONF_USERNAME): cv.string,
		    vol.Required(CONF_PASSWORD): cv.string
			}),
			errors=errors
        )
	