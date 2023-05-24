"""The yarvis integration."""
from __future__ import annotations
from abc import abstractmethod
import re
from homeassistant.components import conversation
from homeassistant.components.conversation.const import HOME_ASSISTANT_AGENT
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import MATCH_ALL
from homeassistant.core import HomeAssistant

from homeassistant.helpers import intent
from homeassistant.components.conversation import AgentManager, agent
from typing import Literal


from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Initialize your integration."""
    conversation.async_set_agent(hass, entry, Yarvis(hass, entry))
    return True


class Yarvis(conversation.AbstractConversationAgent):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the agent."""
        self.hass = hass
        self.entry = entry
        self.history: dict[str, list[dict]] = {}

    @property
    def attribution(self):
        """Return the attribution."""
        return {"name": "Yarvis", "url": "https://www.openai.com"}

    @property
    def supported_languages(self) -> list[str] | Literal["*"]:
        """Return a list of supported languages."""
        return MATCH_ALL

    async def async_process(
        self, user_input: agent.ConversationInput
    ) -> agent.ConversationResult:
        """Process a sentence."""
        intents = self.entry.options["intents"]
        for int_key in intents:
            for sentence in intents[int_key]["sentences"]:
                match = re.search(sentence, user_input.text, re.IGNORECASE)

                if match:
                    slots = {}
                    for key in match.groupdict():
                        slots[key] = {"value": match.group(key)}
                    response = await intent.async_handle(
                        self.hass, DOMAIN, int_key, slots
                    )
                    return agent.ConversationResult(
                        conversation_id=None, response=response
                    )

        return await conversation.async_converse(
            self.hass,
            user_input.text,
            user_input.conversation_id,
            user_input.context,
            None,
            HOME_ASSISTANT_AGENT,
        )
