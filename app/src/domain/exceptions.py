from application.interfaces.exception import ExceptionProtocol


class ModelFoundError(ExceptionProtocol):
    base_msg = "not found"


class OrganizationError(ExceptionProtocol):
    base_msg = "OrganizationError"


class BuildingError(ExceptionProtocol):
    base_msg = "Building error"


class ActivityError(ExceptionProtocol):
    base_msg = "ActivityError"


class OrganizationNotFoundError(ModelFoundError):
    base_msg = "Organization not found"


class BuildingNotFoundError(ModelFoundError):
    base_msg = "Building not found"


class ActivityNotFoundError(ModelFoundError):
    base_msg = "Activity not found"
