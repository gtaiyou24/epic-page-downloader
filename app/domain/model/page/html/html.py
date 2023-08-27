from dataclasses import dataclass

from domain.model.page.html import CharacterCode


@dataclass(init=False, unsafe_hash=True, frozen=True)
class HTML:
    source: str
    character_code: CharacterCode

    def __init__(self, source: str, character_code: CharacterCode):
        super().__setattr__("source", source)
        super().__setattr__("character_code", character_code)

    def is_not_empty(self) -> bool:
        return self.source is not None and self.source != ''
