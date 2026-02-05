from application.interfaces.exception import ExceptionProtocol


class OrganizationError(ExceptionProtocol):
    base_msg = "OrganizationError"


class BuildingError(ExceptionProtocol):
    base_msg = "Building error"


class ActivityError(ExceptionProtocol):
    base_msg = "ActivityError"


class OrganizationNotFoundError(OrganizationError):
    base_msg = "Organization not found"


class BuildingNotFoundError(BuildingError):
    base_msg = "Building not found"


class ActivityNotFoundError(ActivityError):
    base_msg = "Activity not found"
