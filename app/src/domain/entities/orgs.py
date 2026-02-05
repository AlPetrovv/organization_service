from dataclasses import dataclass

from phonenumbers.phonenumber import PhoneNumber

from .base import Entity


@dataclass(kw_only=True, slots=True)
class OrganizationPhoneEntity(Entity[int]):
    number: PhoneNumber
