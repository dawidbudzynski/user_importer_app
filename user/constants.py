import enum

ALLOWED_IMPORT_TYPES = [
    'Subscriber',
    'SubscriberSMS'
]


class ConflictReason(enum.Enum):
    USER_CONFLICT = 'User conflict'
    CLIENT_PHONE_NOT_UNIQUE = 'Client phone not unique'
