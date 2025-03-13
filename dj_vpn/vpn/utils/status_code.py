class ErrorResponse:
    BAD_FORMAT = {'detail': 'BAD_FORMAT', 'error_code': 1}
    OBJECT_NOT_FOUND = {'detail': 'OBJECT_NOT_FOUND', 'error_code': 2}
    WRONG_LOGIN_DATA = {'detail': 'WRONG_USER_LOGIN_DATA', 'error_code': 3}
    INVALID_INPUT = {'detail': 'INVALID_INPUT', 'error_code': 4}
    MISSING_PARAMS = {'detail': 'MISSING_PARAMS', 'error_code': 5}
    TOKEN_IS_EXPIRED_OR_INVALID = {'detail': 'TOKEN_IS_EXPIRED_OR_INVALID', 'error_code': 6}
    CODE_IS_EXPIRED_OR_INVALID = {'detail': 'CODE_IS_EXPIRED_OR_INVALID', 'error_code': 7}
    SOMETHING_WENT_WRONG = {'detail': "WE_ALSO_DON'T_KNOW_WHAT_HAPPENED!", 'error_code': 8}
    LOGIN_BLOCKED = {'detail': 'LOGIN_BLOCKED', 'error_code': 9}
    USER_USAGE_LIMIT = {'detail': 'USER_USAGE_LIMIT', 'error_code': 10}
    FIELD_NOT_ACTIVE = {'detail': 'FIELD_NOT_ACTIVE', 'error_code': 11}
    FIELD_IS_ACTIVE = {"detail": "FIELD_IS_ACTIVE", 'error_code': 12}
    INVALID_PASSWORD = {"detail": "INVALID_PASSWORD", 'error_code': 13}
    MAXIMUM_REACH = {"detail": "MAXIMUM_REACH", 'error_code': 14}
    EXPIRED = {"detail": "EXPIRED", 'error_code': 215}
    LIMIT_REACH = {"detail": "LIMIT", 'error_code': 216}
