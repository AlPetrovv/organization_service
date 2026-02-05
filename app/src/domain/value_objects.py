from dataclasses import dataclass

from geoalchemy2 import WKBElement


@dataclass(kw_only=True, slots=True)
class Location:
    value: WKBElement
