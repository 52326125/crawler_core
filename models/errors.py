from enum import Enum


class Error(str, Enum):
    CRAWLER_NOT_MATCH = "Can't find matched crawler."
    FILE_NAME_EMPTY = "File name is empty."
    CONNECTION_FAILED = "Failed to connection correct url."
    DUPLICATED_USER = "User already exists."
    UNDEFINED_EXCEPTION = "Uncatch exception."
    CREDENTIAL_ERROR = "Could not validate credentials."
    AUTHORIZATION_ERROR = "Authorization failed."
