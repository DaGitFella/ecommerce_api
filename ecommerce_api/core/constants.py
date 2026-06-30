import enum


class UserRole(enum.Enum):
    CUSTOMER = 'customer'
    EMPLOYEE = 'employee'
    ADMIN = 'admin'
    GUEST = 'guest'


class ShippingTypes(enum.Enum):
    DELIVERY = 'delivery'
    PICKUP = 'pickup'


class RepairJobStatus(enum.Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    WAITING_PARTS = 'waiting_parts'
    WAITING_PAYMENT = 'waiting_payment'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
