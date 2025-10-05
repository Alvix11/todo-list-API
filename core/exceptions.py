from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated

def custom_exception_handler(exc, context):
    """
    Handles exceptions globally so as not to display so much information
    """
    response = exception_handler(exc, context)
    
    if isinstance(exc, NotAuthenticated):
        return Response(
            {"message": "Forbidden"},
            status=status.HTTP_403_FORBIDDEN
            )
        
    elif isinstance(exc, AuthenticationFailed):
        return Response(
            {"message": "Unauthorized"},
            status=status.HTTP_401_UNAUTHORIZED
            )
    
    return response
