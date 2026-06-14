import enum


class UserRole(enum.Enum):
    CUSTOMER = 'customer'
    EMPLOYEE = 'employee'
    ADMIN = 'admin'
    GUEST = 'guest'


class ShippingTypes(enum.Enum):
    DELIVERY = 'delivery'
    PICKUP = 'pickup'
