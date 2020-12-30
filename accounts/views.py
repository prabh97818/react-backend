from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken
from itsdangerous import TimedJSONWebSignatureSerializer as TokenSerializer
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

def get_active_token(user_id, expires_sec=3600*24*30):
    s = TokenSerializer(settings.SECRET_KEY, expires_sec)
    return s.dumps({'user_id': user_id}).decode('utf-8')

@api_view(['GET'])
@permission_classes([])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """
    try:
        username = request.GET.get('username')
        usr = User.objects.get(username=username)
    except:
        usr = request.user
    serializer = UserSerializer(usr)
    return Response(serializer.data)

@api_view(['GET', 'DELETE', 'PUT'])
def all_users(request):
    """
    Get list of all users
    """
    if request.method =="GET":
        alluser = User.objects.all()
        serializer = UserSerializer(alluser, many=True )
        return Response(serializer.data)

    if request.method =="DELETE":
        username = request.GET.get('username')
        deluser = User.objects.get(username=username).delete()
        if deluser:
            data={"Success":"User Deleted"}
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data={"failed":"Deletion Failed"}
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method =="PUT":
        username = request.GET.get('username')
        edituser = User.objects.get(username=username)
        if edituser:
            serializer = UserSerializer(edituser, data=request.data)
            if serializer.is_valid():
                serializer.save()
                data={"Success":"User Updated"}
                return Response(data, status=status.HTTP_201_CREATED)
        else:
            data={"failed":"Failed"}
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserList(APIView):
    """
    Add User  
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_active=False)
            approval_token = get_active_token(user.id)


            # verify_url = settings.CLIENT_URL+'/api/approve-account/' + approval_token
            verify_url = settings.CLIENT_URL+'/verifyAccount/' + approval_token
                
                
            subject = 'Registration Request - MyApp'

            msg_plain = render_to_string('accounts/email-verification.txt', {'verify_url': verify_url})
            msg_html = render_to_string('accounts//email-verification.html', {'verify_url': verify_url})  
            recepient = [user.email,]

            if True:
                send_mail(
                    subject,
                    msg_plain,
                    'settings.EMAIL_HOST_USER',
                    recepient,
                    html_message=msg_html,
                )
                data = {
                    "success":"An email with account activation link has sent to your email. Please check your email to activate your account!"
                }             
            else:
                data = {
                    "failed":"Sorry, we are unable to send you an activation email at the moment. Please try again after sometime"
                }

            return Response(data, status=status.HTTP_201_CREATED)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def approve_account(request, token):
    s = TokenSerializer(settings.SECRET_KEY)
    approved = False
    try:
        user_id = s.loads(token)['user_id']
        new_user = User.objects.get(id = user_id)
        if not new_user.is_active:
            new_user.is_active = True
            
            new_user.save()
            data = {
                    "success":"Your account is activated. Login now!"
                }  
        else:
            data = {
                    "success":"Your account is already active!"
                }  
                        
    except:
        data = {
                    "failed":"Invalid or expired request!"
                } 
    return JsonResponse(data)