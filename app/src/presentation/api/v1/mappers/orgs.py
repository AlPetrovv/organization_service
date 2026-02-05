import phonenumbers

from domain.agregates import OrganizationEntity
from domain.entities.orgs import OrganizationPhoneEntity
from presentation.api.v1.mappers.activities import ActivityApiMapper
from presentation.api.v1.mappers.buildings import BuildingApiMapper
from presentation.api.v1.schemas.orgs import OrganizationResponse, OrganizationResponseDetail, OrganizationPhone
from pydantic_extra_types.phone_numbers import PhoneNumber


class OrganizationPhoneNumbersApiMapper:
    def to_response(self, phone_numbers: list[OrganizationPhoneEntity]) -> list[OrganizationPhone]:
        response = [
            OrganizationPhone(
                id=phone_number.id,
                number=PhoneNumber(
                    phonenumbers.format_number(phone_number.number, phonenumbers.PhoneNumberFormat.E164)
                ),
            )
            for phone_number in phone_numbers
        ]
        return response


class OrganizationApiMapper:
    def __init__(self):
        self.activity_mapper = ActivityApiMapper()
        self.building_mapper = BuildingApiMapper()
        self.phone_numbers_mapper = OrganizationPhoneNumbersApiMapper()

    def to_detail_response(self, entity: OrganizationEntity) -> OrganizationResponseDetail:
        building = self.building_mapper.to_response(entity.building)
        phone_numbers = self.phone_numbers_mapper.to_response(entity.phones)
        activities = [self.activity_mapper.to_response(activity) for activity in entity.activities]
        response = OrganizationResponseDetail(
            id=entity.id, name=entity.name, phone_numbers=phone_numbers, building=building, activities=activities
        )
        return response

    def to_response(self, entity: OrganizationEntity) -> OrganizationResponse:
        response = OrganizationResponse(id=entity.id, name=entity.name)
        return response
