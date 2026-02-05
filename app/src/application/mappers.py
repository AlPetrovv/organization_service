from application.dto.activities import ActivityDTO
from application.dto.buildings import BuildingDTO, LocationDTO
from application.dto.orgs import OrganizationDTO, OrganizationPhoneDTO
from application.interfaces.mapper import DataMapper
from domain.entities.activities import ActivityEntity
from domain.entities.buildings import BuildingEntity
from domain.agregates import OrganizationEntity, OrganizationPhoneEntity


class ActivityMapper(DataMapper[ActivityDTO]):
    dto_class = ActivityDTO

    def to_dto(self, entity: ActivityEntity) -> ActivityDTO:
        activity_dto = self.dto_class(name=entity.name, parent_id=entity.parent_id, depth=entity.depth)
        return activity_dto

    def dto_to_dict(self, dto: ActivityDTO) -> dict:
        return {
            "name": dto.name,
            "parent_id": dto.parent_id,
            "depth": dto.depth,
        }

    def entity_to_dict(self, entity: ActivityEntity) -> dict:
        return {
            "id": entity.id,
            "name": entity.name,
            "parent_id": entity.parent_id,
            "depth": entity.depth,
        }


class BuildingMapper(DataMapper[BuildingDTO]):
    dto_class = BuildingDTO

    def to_dto(self, entity: BuildingEntity) -> BuildingDTO:
        location_dto = LocationDTO(value=entity.location.value)
        building_dto = self.dto_class(address=entity.address, location=location_dto)
        return building_dto

    def dto_to_dict(self, dto: BuildingDTO) -> dict:
        return {
            "address": dto.address,
            "location": dto.location.value,
        }

    def entity_to_dict(self, entity: BuildingEntity) -> dict:
        return {"id": entity.id, "address": entity.address, "location": entity.location.value}


class OrganizationPhoneMapper(DataMapper[OrganizationPhoneDTO]):
    dto_class = OrganizationPhoneDTO

    def to_dto(self, entity: OrganizationPhoneEntity) -> OrganizationPhoneDTO:
        return OrganizationPhoneDTO(number=entity.number)

    def dto_to_dict(self, dto: OrganizationPhoneDTO) -> dict:
        return {"number": dto.number}

    def entity_to_dict(self, entity: OrganizationPhoneEntity) -> dict:
        return {"id": entity.id, "number": entity.number}


class OrganizationMapper(DataMapper[OrganizationDTO]):
    dto_class = OrganizationDTO

    def __init__(self):
        self.building_mapper = BuildingMapper()
        self.phone_number_mapper = OrganizationPhoneMapper()
        self.activity_mapper = ActivityMapper()

    def to_dto(self, entity: OrganizationEntity) -> OrganizationDTO:
        building_dto = self.building_mapper.to_dto(entity.building)
        activities_dto = [self.activity_mapper.to_dto(activity_entity) for activity_entity in entity.activities]
        event_dto = self.dto_class(
            name=entity.name,
            created_at=entity.created_at,
            building=building_dto,
            phones=entity.phones,
            activities=activities_dto,
        )
        return event_dto

    def dto_to_dict(self, dto: OrganizationDTO) -> dict:
        return {
            "name": dto.name,
            "created_at": dto.created_at,
            "building": self.building_mapper.dto_to_dict(dto.building),
            "phones": [self.phone_number_mapper.dto_to_dict(phone) for phone in dto.phones],
        }

    def entity_to_dict(self, entity: "OrganizationEntity") -> dict:
        return {
            "id": entity.id,
            "name": entity.name,
            "created_at": entity.created_at,
            "building": self.building_mapper.entity_to_dict(entity.building),
            "phones": [self.phone_number_mapper.entity_to_dict(phone) for phone in entity.phones],
        }
