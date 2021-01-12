import json
import re

from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, parser_classes
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _
from django_currentuser.middleware import get_current_authenticated_user
from rest_framework_simplejwt.exceptions import InvalidToken

from rest_framework_simplejwt.tokens import RefreshToken

from django.conf import settings

from users.models import User
from sit.models import Sit
from users.serializers import *
from django.core.mail import send_mail


def is_password_valid(password):

    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$"
    match_re = re.compile(reg)

    res = re.search(match_re, str(password))

    if res:
        return True
    else:
        return False

def getActivationMail(email, password, username):
    message = '<html><body>' + str(_('<p>Bonjour,<br/><br/> Merci de bien recevoir vos identifiants de connexions,<br/>'
                                     ' username: ')) + str('<b>' + str(username) + '</b><br/>') + str('password : '
                                                                                                           '<b>' + str(
        password) + '</b><br/><br/>') + '' + str(_('Best regards')) + str(
        '</p><p style="color:#DB7D34">Team Digidex</p></body></html>')

    from smtplib import SMTPAuthenticationError
    try:
        send_mail(subject=_('Digidex creation du compte'), message=message,
                  from_email="DIGIDEX<" + settings.DEFAULT_FROM_EMAIL + ">",
                  recipient_list=[email],
                  html_message=message, fail_silently=False)
    except SMTPAuthenticationError:
        return Response({'message': _('Digidex creation du compte')}, status=status.HTTP_423_LOCKED)




@api_view(['POST'])
def connectionFunctionView(request, format=None):
    """
     connection with username and password
    """
    serializer = AccountUsernameSerializer(data=request.data)

    if serializer.is_valid():
        try:

            current_user = get_object_or_404(User, username=serializer.validated_data['username'], password=serializer.validated_data['password'])

            user_serialized = UserSerializer(current_user).data

            user = User.objects.get(username=serializer.validated_data['username'])
            refresh = RefreshToken.for_user(user)
            return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'response': "Aucun compte n'est associe à ses informations"},
                            status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class AccountEmailViewSet(viewsets.ModelViewSet):
    permission_classes = ()
    authentication_classes = ()
    queryset = User.objects.all()
    www_authenticate_realm = 'api'
    serializer_class = AccountEmailSerializer
    http_method_names = ['post', 'put', 'get']

    def list(self, request, *args, **kwargs):
        Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    def create(self, request, *args, **kwargs):

        serializer = AccountEmailSerializer(data=request.data)

        if serializer.is_valid():
            user = User(
                username=serializer.validated_data['email'],
                email=serializer.validated_data['email'],
                is_active=False
            )

            user.set_password(serializer.validated_data['password'])
            token = str(RefreshToken.for_user(user).access_token)

            # message = '<html><body>'+str(_('<p>Salut,<br/><br/> Merci de bien recevoir vos identifiants de connexions,'
            #                                ' Nous vous invitons à cliquer sur le lien  to: '))+str('<a href="'+settings.API_BASE_URL+'/account/email/verify/?token='+token+'&profil='+str(user.id)+'">'+str(_('Click here'))+'</a><br/><br/>')+str(_('Best regards'))+str('</p><p style="color:#DB7D34">Team Digidex</p></body></html>')
            message = '<html><body>'+str(_('<p>Salut,<br/><br/> Merci de bien recevoir vos identifiants de connexions,'
                                           ' username: '))+str('<b>'+str(user.username)+'</b><br/>')+str('password : '
                                          '<b>'+str(user.password)+'</b><br/><br/>')+''+str(_('Best regards'))+str('</p><p style="color:#DB7D34">Team Digidex</p></body></html>')

            from smtplib import SMTPAuthenticationError
            try:
                send_mail(subject=_('Digidex creation du compte'), message=message, from_email="IZYCAB<"+settings.DEFAULT_FROM_EMAIL+">", recipient_list=[serializer.validated_data['email']],
                          html_message=message, fail_silently=False)
                user.save()
            except SMTPAuthenticationError:
                return Response({'message': _('Digidex creation du compte')}, status=status.HTTP_423_LOCKED)
            user_serialized = UserSerializer(user).data
            return Response(user_serialized, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False,)
    def verify(self, request, *args, **kwargs):
        token = request.GET['token']
        user = request.GET['profil']

        from rest_framework_simplejwt.authentication import JWTAuthentication
        try:
            JWTAuthentication.get_validated_token(self, token)
            User.objects.filter(pk=user).update(is_active=True)
            return Response(_('Account verified'), status=status.HTTP_200_OK)
        except InvalidToken:
            return Response(InvalidToken.default_detail, status=InvalidToken.status_code)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #http_method_names = ['get', 'post', 'put', 'delete']
    http_method_names = ['get', 'put', ]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = [ 'email', 'last_name', 'first_name']
    search_fields = [ '=email', '^last_name', '^first_name']
    ordering_fields = ['created', 'modified']

    # def create(self, request, *args, **kwargs):
    #
    #     serializer = UserSerializer(data=request.data)
    #
    #     if serializer.is_valid():
    #
    #         user = User(
    #             username=serializer.validated_data['email'],
    #             first_name=None if 'first_name' not in serializer.validated_data else serializer.validated_data['first_name'],
    #             last_name=None if 'last_name' not in serializer.validated_data else serializer.validated_data['last_name'],
    #             email=serializer.validated_data['email'],
    #             avatar=None if 'avatar' not in serializer.validated_data else serializer.validated_data['avatar'],
    #         )
    #         #user.set_password(serializer.validated_data['password'])
    #         if 'password' in serializer.validated_data:
    #             user.set_password(serializer.validated_data['password'])
    #
    #             if not is_password_valid(serializer.validated_data['password']):
    #                 return Response({"details": _("The password must contain at least 1 uppercase letter, 1 special character and a minimum length of 8 characters")}, status=status.HTTP_400_BAD_REQUEST)
    #         else:
    #             return Response({"details": _("Please provide a password")}, status=status.HTTP_400_BAD_REQUEST)
    #         user.save()
    #
    #         user_serialized = UserSerializer(user).data
    #
    #         return Response(user_serialized, status=status.HTTP_201_CREATED)
    #     else:
    #
    #         return Response(serializer.errors,
    #                         status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @action(detail=False, methods=['post'], serializer_class=AccountUsernameSerializer)
    def connexion(self, request, *args, **kwargs):
        """
         connection with username and password
        """
        user = self.get_object()
        serializer = AccountUsernameSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], serializer_class=PasswordSerializer)
    def change_password(self, request, *args, **kwargs):
        """
         Change user password by providing old_password and new_password. The minimun length is 8
         In addition, the password must have at least one uppercase letter, one number and one special character
        """
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        user_serializer = UserSerializer(user)

        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return Response({"old_password": ["Votre ancienne mot de passe ne correspond pas"]}, status=status.HTTP_400_BAD_REQUEST)

            if is_password_valid(serializer.data.get('new_password')):
                user.set_password(serializer.data.get('new_password'))
                site = get_object_or_404(Sit, pk=serializer.data.get('sit'))
                user.sit = site
                user.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({"details": _("The password must contain at least 1 uppercase letter, 1 special character and a minimum length of 8 characters")}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False, url_path='me', url_name='me')
    def me(self, request, *args, **kwargs):

        try:
            User.objects.get(Q(username=get_current_authenticated_user()) )

            current_user = get_object_or_404(User, username=get_current_authenticated_user())

            user_serialized = UserSerializer(current_user).data

            return Response(user_serialized)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # @action(methods=['GET'], detail=True, url_path='enable', url_name='enable', serializer_class=UserSerializer)
    # def enable(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     User.objects.filter(pk=instance.id).update(is_active=True)
    #     serializer = self.get_serializer(User.objects.filter(pk=instance.id))
    #     return Response()
    #
    # @action(methods=['GET'], detail=True, url_path='disable', url_name='disable', serializer_class=UserSerializer)
    # def disable(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     User.objects.filter(pk=instance.id).update(is_active=False)
    #     serializer = self.get_serializer(User.objects.filter(pk=instance.id))
    #     return Response()





