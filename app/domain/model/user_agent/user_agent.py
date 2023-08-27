from __future__ import annotations

import dataclasses

from random_user_agent.params import HardwareType, SoftwareName
from random_user_agent.user_agent import UserAgent as RandomUserAgent

from domain.model.user_agent import Device


@dataclasses.dataclass(init=False, unsafe_hash=True, frozen=True)
class UserAgent:
    value: str

    def __init__(self, value: str):
        assert value, 'ユーザーエージェントに文字列を指定してください。'
        super().__setattr__('value', value)

    @staticmethod
    def random(device: Device) -> UserAgent:
        if device == Device.SP:
            hardware_types = [HardwareType.MOBILE.value]
        else:
            hardware_types = [HardwareType.COMPUTER.value]

        ua = RandomUserAgent(
            hardware_types=hardware_types,
            software_names=[
                SoftwareName.CHROME.value,
                SoftwareName.FIREFOX.value,
                SoftwareName.INTERNET_EXPLORER.value,
                SoftwareName.SAFARI.value
            ]
        )
        return UserAgent(ua.get_random_user_agent())
