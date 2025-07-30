from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext_lazy as _

from utils.jcode import SUCCESS

def data_response(status_code=SUCCESS, message="OK", data=None, errors=None):
    response = {
        "status": status_code,
        "message": message,
    }
    if data is not None:
        response["data"] = data
    if errors:
        response["errors"] = errors
    return response

def response_data(status=status.HTTP_200_OK, status_code=SUCCESS, message="OK", data=None, errors=None):
    return Response(
        status=status,
        data=data_response(status_code=status_code, message=message, data=data, errors=errors)
    )

def response_message(message, status=status.HTTP_200_OK):
    return response_data(status_code=SUCCESS, message=_(message), status=status)