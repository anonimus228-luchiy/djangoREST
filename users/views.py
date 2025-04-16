from rest_framework import status
from .serializers import UserAuthSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import random
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import ConfirmationCode
@api_view(['POST'])
def authentication_api_view(request):
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data('username')
    password = serializer.validated_data('password')

    user = authenticate(**serializer.validated_data)

    if user is not None:
        try:
            token = Token.objects.get_or_create(user=user)
        except:
            token = Token.objects.create(user=user)
            return Response(data={'key':token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED,
                    data={'error':'Invalid username or'})



@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'})

    user = User.objects.create_user(username=username, password=password, is_active=False)

    code = str(random.randint(100000, 999999))
    ConfirmationCode.objects.create(user=user, code=code)

    return Response({'message': 'User created', 'code': code})


@api_view(['POST'])
def confirm(request):
    username = request.data.get('username')
    code = request.data.get('code')

    try:
        user = User.objects.get(username=username)
        confirmation = ConfirmationCode.objects.get(user=user)
    except:
        return Response({'error': 'Invalid user or code'}, status=400)

    if confirmation.code == code:
        user.is_active = True
        user.save()
        confirmation.delete()
        return Response({'message': 'Confirmed'})
    else:
        return Response({'error': 'Wrong code'})
