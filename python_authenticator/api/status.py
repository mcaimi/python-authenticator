#
# TOTP authenticator API server
# HTTP Status codes
#
# v0.1 -- Marco Caimi <mcaimi@redhat.com>
#

""" HTTP Status Codes """

HTTP_100_CONTINUE = 100
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_202_ACCEPTED = 202
HTTP_204_NO_CONTENT = 204
HTTP_301_MOVED_PERMANENTLY = 301
HTTP_302_FOUND = 302
HTTP_400_BAD_REQUEST = 400
HTTP_401_UNAUTHORIZED = 401
HTTP_403_FORBIDDEN = 403
HTTP_404_NOT_FOUND = 404
HTTP_405_METHOD_NOT_ALLOWED = 405
HTTP_500_SERVER_ERROR = 500
HTTP_501_NOT_IMPLEMENTED = 501


def is_informational_code(statuscode: int) -> bool:
    ''' response contains an informational code '''
    return 100 <= statuscode <= 199


def is_success_code(statuscode: int) -> bool:
    ''' response contains an successful code '''
    return 200 <= statuscode <= 299


def is_redirection_code(statuscode: int) -> bool:
    ''' response contains a redirection code '''
    return 300 <= statuscode <= 399


def is_client_error_code(statuscode: int) -> bool:
    ''' response contains a client error code '''
    return 400 <= statuscode <= 499


def is_server_error_code(statuscode: int) -> bool:
    ''' response contains a server error code '''
    return 500 <= statuscode <= 599
