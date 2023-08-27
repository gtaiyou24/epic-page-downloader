from __future__ import annotations

from enum import Enum


class Device(Enum):
    SP = 'SP'
    PC = 'PC'

    @staticmethod
    def value_of(name: str) -> Device:
        for e in Device:
            if e.value == name:
                return e
        raise ValueError(f'{name}に一致するDeviceは見つかりません。')
