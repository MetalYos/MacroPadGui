from dataclasses import dataclass, field

@dataclass
class MacroPadKey:
    row: int
    col: int
    keycode: int
    is_modifier: bool

@dataclass
class MacroPadStruct:
    keys: list[MacroPadKey] = field(default_factory=list())