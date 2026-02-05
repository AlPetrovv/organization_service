from typing import TYPE_CHECKING

from phonenumbers.phonenumberutil import format_number, PhoneNumberFormat

from application.interfaces.db_mapper import DBMapperProtocol

from domain.agregates import OrganizationEntity
from domain.entities.orgs import OrganizationPhoneEntity
from infra.resouces.database.mappers.activities import DBActivityMapper
from infra.resouces.database.mappers.buildings import DBBuildingMapper
from infra.resouces.database.models import Organization, OrganizationPhoneNumber, Building

if TYPE_CHECKING:
    from application.dto.orgs import OrganizationDTO, OrganizationPhoneDTO


class DBPhoneMapper(DBMapperProtocol):
    def to_entity(self, phone: OrganizationPhoneNumber) -> OrganizationPhoneEntity:
        return OrganizationPhoneEntity(id=phone.id, number=phone.phone)

    def to_model(self, entity: "OrganizationPhoneEntity") -> "OrganizationPhoneNumber":
        return OrganizationPhoneNumber(id=entity.id, phone=entity.number)

    def to_model_from_dto(self, dto: "OrganizationPhoneDTO"):
        return OrganizationPhoneNumber(
            phone=format_number(
                dto.number,
                PhoneNumberFormat.E164,
            )
        )

    def update_model_from_entity(self, phone: OrganizationPhoneNumber, entity: OrganizationPhoneEntity) -> None:
        phone.number = entity.number


class DBOrganizationMapper(DBMapperProtocol):
    def __init__(self):
        self.building_mapper = DBBuildingMapper()
        self.phone_mapper = DBPhoneMapper()
        self.activity_mapper = DBActivityMapper()

    def to_entity(self, org: Organization) -> OrganizationEntity:
        build_entity = self.building_mapper.to_entity(org.building)

        phones = [self.phone_mapper.to_entity(phone) for phone in org.phones]
        return OrganizationEntity(
            id=org.id,
            name=org.name,
            created_at=org.created_at,
            phones=phones,
            building=build_entity,
        )

    def to_model(self, entity: OrganizationEntity) -> Organization:
        building = self.building_mapper.to_model(entity.building)
        return Organization(id=entity.id, created_at=entity.created_at, building=building)

    def to_model_from_dto(self, dto: "OrganizationDTO"):
        phones = [self.phone_mapper.to_model_from_dto(phone) for phone in dto.phones]
        activities = [self.activity_mapper.to_model_from_dto(activity) for activity in dto.activities]
        building = self.building_mapper.to_model_from_dto(dto.building)

        return Organization(
            name=dto.name, created_at=dto.created_at, phones=phones, activities=activities, building=building
        )

    def update_model_from_entity(self, org: Organization, entity: OrganizationEntity) -> None:
        org.name = entity.name

        org.created_at = entity.created_at
        if org.building is None:
            org.building = Building()
        self.building_mapper.update_model_from_entity(org.building, entity.building)
