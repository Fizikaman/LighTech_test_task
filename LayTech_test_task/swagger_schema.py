from drf_yasg import openapi

TOKENS_PARAMETER = \
    {
        'manual_parameters': [
            openapi.Parameter('AUTHORIZATION', openapi.IN_HEADER, type=openapi.TYPE_STRING, required=True,
                              description='Access Token(формат: Token + token)'),
            openapi.Parameter('REFRESH', openapi.IN_HEADER, type=openapi.TYPE_STRING, required=False,
                              description='Refresh Token'),

        ],
    }