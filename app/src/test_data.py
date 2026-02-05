import phonenumbers
from dependency_injector.wiring import inject, Provide
from geoalchemy2.elements import WKTElement


from application.dto.activities import ActivityDTO
from application.dto.buildings import BuildingDTO, LocationDTO
from application.dto.orgs import OrganizationDTO, OrganizationPhoneDTO


from ioc import Container


@inject
async def create_test_data(ouw=Provide[Container.db.uow]):
    """Create test data. convert into migration or tests later"""
    async with ouw:
        try:
            location_1 = LocationDTO(value=WKTElement(data="POINT(1 1)", srid=4326))
            location_2 = LocationDTO(value=WKTElement(data="POINT(0 0)", srid=4326))
            building_dto_1 = BuildingDTO(address="test_address_1", location=location_1)
            building_dto_2 = BuildingDTO(address="test_address_2", location=location_2)
            activity_d1 = await ouw.activities.create(ActivityDTO(name="test", depth=1))
            activity_d2 = await ouw.activities.create(ActivityDTO(name="test_d2", depth=2, parent_id=activity_d1.id))
            activity_dto_d3 = ActivityDTO(name="test_d3", depth=3, parent_id=activity_d2.id)
            activity_dto_d4 = ActivityDTO(name="test_d4", depth=3, parent_id=activity_d2.id)
            org_1_phones = [
                OrganizationPhoneDTO(
                    number=phonenumbers.parse(
                        "+77001234567",
                    ),
                ),
                OrganizationPhoneDTO(number=phonenumbers.parse("+77001234568")),
            ]
            org_2_phones = [
                OrganizationPhoneDTO(
                    number=phonenumbers.parse("+77001234565"),
                ),
                OrganizationPhoneDTO(number=phonenumbers.parse("+77001234566")),
            ]
            await ouw.organizations.create(
                OrganizationDTO(
                    name="test", phones=org_1_phones, building=building_dto_1, activities=[activity_dto_d3]
                )
            )
            await ouw.organizations.create(
                OrganizationDTO(
                    name="test2", phones=org_2_phones, building=building_dto_2, activities=[activity_dto_d4]
                )
            )
        except Exception as e:
            await ouw.session.rollback()
            await ouw.session.close()
