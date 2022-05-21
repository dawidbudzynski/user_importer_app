import enum


class ConflictReason(enum.Enum):
    USER_CONFLICT = 'User conflict',
    CLIENT_PHONE_NOT_UNIQUE = 'Client phone not unique'
