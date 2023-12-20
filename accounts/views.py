import requests
import jwt
from json.decoder import JSONDecodeError

from django.shortcuts import redirect, get_object_or_404
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from rest_framework import viewsets, mixins, generics, permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from boonglunteer.settings import SECRET_KEY
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.models import SocialAccount

from .models import User
from .serializers import *


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    # 유저 정보 확인
    def get(self, request):
        try:
            # access token을 decode 해서 유저 id 추출 => 유저 식별
            access = request.COOKIES['access']
        except KeyError:
            # 'access' 키가 존재하지 않을 때의 처리
            return Response({'error': 'Access token not provided'}, status=status.HTTP_400_BAD_REQUEST)
        try:
        #     # access token을 decode 해서 유저 id 추출 => 유저 식별
        #     access = request.COOKIES['access']
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            data = {'refresh': request.COOKIES.get('refresh', None)}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access', None)
                refresh = serializer.data.get('refresh', None)
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)
                serializer = UserSerializer(instance=user)
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie('access', access)
                res.set_cookie('refresh', refresh)
                return res
            raise jwt.exceptions.InvalidTokenError

        except(jwt.exceptions.InvalidTokenError):
            # 사용 불가능한 토큰일 때
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # 로그인
    def post(self, request):
    	# 유저 인증
        user = authenticate(
            email=request.data.get("email"), password=request.data.get("password")
        )
        # 이미 회원가입 된 유저일 때
        if user is not None:
            serializer = UserSerializer(user)
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    def get(self, request):
        try:
            # access token을 decode 해서 유저 id 추출 => 유저 식별
            access = request.COOKIES['access']
        except KeyError:
            # 'access' 키가 존재하지 않을 때의 처리
            return Response({'error': 'Access token not provided'}, status=status.HTTP_400_BAD_REQUEST)
        try:
        #     # access token을 decode 해서 유저 id 추출 => 유저 식별
        #     access = request.COOKIES['access']
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            data = {'refresh': request.COOKIES.get('refresh', None)}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access', None)
                refresh = serializer.data.get('refresh', None)
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)
                serializer = UserSerializer(instance=user)
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie('access', access)
                res.set_cookie('refresh', refresh)
                return res
            raise jwt.exceptions.InvalidTokenError

        except(jwt.exceptions.InvalidTokenError):
            # 사용 불가능한 토큰일 때
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
        response = Response({
            "message": "Logout success"
            }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response

# class AuthAPIView(APIView):
    # # 유저 정보 확인
    # def get(self, request):
    #     try:
    #         # access token을 decode 해서 유저 id 추출 => 유저 식별
    #         access = request.COOKIES['access']
    #     except KeyError:
    #         # 'access' 키가 존재하지 않을 때의 처리
    #         return Response({'error': 'Access token not provided'}, status=status.HTTP_400_BAD_REQUEST)
    #     try:
    #     #     # access token을 decode 해서 유저 id 추출 => 유저 식별
    #     #     access = request.COOKIES['access']
    #         payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
    #         pk = payload.get('user_id')
    #         user = get_object_or_404(User, pk=pk)
    #         serializer = UserSerializer(instance=user)
    #         return Response(serializer.data, status=status.HTTP_200_OK)

    #     except(jwt.exceptions.ExpiredSignatureError):
    #         # 토큰 만료 시 토큰 갱신
    #         data = {'refresh': request.COOKIES.get('refresh', None)}
    #         serializer = TokenRefreshSerializer(data=data)
    #         if serializer.is_valid(raise_exception=True):
    #             access = serializer.data.get('access', None)
    #             refresh = serializer.data.get('refresh', None)
    #             payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
    #             pk = payload.get('user_id')
    #             user = get_object_or_404(User, pk=pk)
    #             serializer = UserSerializer(instance=user)
    #             res = Response(serializer.data, status=status.HTTP_200_OK)
    #             res.set_cookie('access', access)
    #             res.set_cookie('refresh', refresh)
    #             return res
    #         raise jwt.exceptions.InvalidTokenError

    #     except(jwt.exceptions.InvalidTokenError):
    #         # 사용 불가능한 토큰일 때
    #         return Response(status=status.HTTP_400_BAD_REQUEST)

    # # 로그인
    # def post(self, request):
    # 	# 유저 인증
    #     user = authenticate(
    #         email=request.data.get("email"), password=request.data.get("password")
    #     )
    #     # 이미 회원가입 된 유저일 때
    #     if user is not None:
    #         serializer = UserSerializer(user)
    #         # jwt 토큰 접근
    #         token = TokenObtainPairSerializer.get_token(user)
    #         refresh_token = str(token)
    #         access_token = str(token.access_token)
    #         res = Response(
    #             {
    #                 "user": serializer.data,
    #                 "message": "login success",
    #                 "token": {
    #                     "access": access_token,
    #                     "refresh": refresh_token,
    #                 },
    #             },
    #             status=status.HTTP_200_OK,
    #         )
    #         # jwt 토큰 => 쿠키에 저장
    #         res.set_cookie("access", access_token, httponly=True)
    #         res.set_cookie("refresh", refresh_token, httponly=True)
    #         return res
    #     else:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)

    # 로그아웃
    # def delete(self, request):
    #     # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
    #     response = Response({
    #         "message": "Logout success"
    #         }, status=status.HTTP_202_ACCEPTED)
    #     response.delete_cookie("access")
    #     response.delete_cookie("refresh")
    #     return response

# state = getattr(settings, 'STATE')

# BASE_URL = 'http://localhost:8000/'
# GOOGLE_CALLBACK_URI = BASE_URL + 'accounts/google/callback/'

# def google_login(request):
#     """
#     Code Request
#     """
#     scope = "https://www.googleapis.com/auth/userinfo.email"
#     client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
#     return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")

# def google_callback(request):
#     client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
#     client_secret = getattr(settings, "SOCIAL_AUTH_GOOGLE_SECRET")
#     print(client_id, client_secret)
#     code = request.GET.get('code')
#     """
#     Access Token Request
#     """
#     token_req = requests.post(f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")
#     token_req_json = token_req.json()
#     error = token_req_json.get("error")
#     if error is not None:
#         raise JSONDecodeError(error)
#     access_token = token_req_json.get('access_token')
#     """
#     Email Request
#     """
#     # access_token = request.data.get("access_token")
#     email_req = requests.get(
#     f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
#     email_req_status = email_req.status_code

#     if email_req_status != 200:
#         return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)

#     email_req_json = email_req.json()
#     email = email_req_json.get('email')
#     """
#     Signup or Signin Request
#     """
#     try:
#         user = User.objects.get(email=email)
#         social_user = SocialAccount.objects.get(user=user)

#         # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
#         # 다른 SNS로 가입된 유저
#         if social_user is None:
#             return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
#         if social_user.provider != 'google':
#             return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
#         # 기존에 Google로 가입된 유저
#         data = {'access_token': access_token, 'code': code}
#         print(data)
#         accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=data)
#         accept_status = accept.status_code

#         if accept_status != 200:
#             return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)

#         accept_json = accept.json()
#         print(accept)
#         accept_json.pop('user', None)
#         return JsonResponse(accept_json)

#     except User.DoesNotExist:
#         # 기존에 가입된 유저가 없으면 새로 가입
#         data = {'access_token': access_token, 'code': code}

#         accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=data)

#         accept_status = accept.status_code

#         if accept_status != 200:
#             return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
#         accept_json = accept.json()
#         accept_json.pop('user', None)
#         return JsonResponse(accept_json)

# class GoogleAccessView(APIView):
#     def post(self, request):
#         access_token = request.data.get("access_token")
#         email_req = requests.get(
#         f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
#         email_req_status = email_req.status_code

#         if email_req_status != 200:
#             return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)

#         email_req_json = email_req.json()
#         email = email_req_json.get('email')
#         """
#         Signup or Signin Request
#         """
#         try:
#             user = User.objects.get(email=email)
#             social_user = SocialAccount.objects.get(user=user)

#             # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
#             # 다른 SNS로 가입된 유저
#             if social_user is None:
#                 return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
#             if social_user.provider != 'google':
#                 return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)

#             data = {'access_token': access_token}
#             print(data)
#             accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=data)
#             accept_status = accept.status_code

#             if accept_status != 200:
#                 return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)

#             accept_json = accept.json()
#             # accept_json.pop('user', None)
#             return JsonResponse(accept_json)

#         except User.DoesNotExist:
#             # 기존에 가입된 유저가 없으면 새로 가입
#             # data = {'access_token': access_token, 'code': code}
#             data = {'access_token': access_token}
#             accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=data)
#             accept_status = accept.status_code

#             if accept_status != 200:
#                 return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
#             accept_json = accept.json()
#             # accept_json.pop('user', None)
#             return JsonResponse(accept_json)


# class GoogleLogin(SocialLoginView):
#     adapter_class = google_view.GoogleOAuth2Adapter
#     callback_url = GOOGLE_CALLBACK_URI
#     permission_classes = [AllowAny]
#     client_class = OAuth2Client


# ############################
# ####### 사용자 Views ########
# ############################
        
# class UserViewSet(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSeriazlier
    
#     def get_object(self):
#         return get_object_or_404(User, id=self.request.user.id)
    
# class UserBankViewSet(generics.UpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserBankSerializer
    
#     def get_object(self):
#         return get_object_or_404(User, id=self.request.user.id)
    
# class UserDateViewSet(generics.UpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserDateSerializer
    
#     def get_object(self):
#         return get_object_or_404(User, id=self.request.user.id)

# class UserFishbreadViewSet(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserFishbreadSerializer

#     def get_qureryset(self):
#         return get_object_or_404(User, id=self.request.user.id)







# class UserListView(generics.ListAPIView):
#     queryset = get_user_model().objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]

# class UserCreateView(generics.CreateAPIView):
#     serializer_class = UserCreateSerializer
#     permission_classes = [permissions.AllowAny]

#     def create(self, request, *args, **kwargs):
#         # 기본 create 메소드 호출
#         response = super().create(request, *args, **kwargs)

#         # 사용자 생성 후 토큰 생성
#         if response.status_code == status.HTTP_201_CREATED:
#             user = get_user_model().objects.get(email=response.data['email'])
#             token, created = Token.objects.get_or_create(user=user)
#             response.data['token'] = token.key

#         return response

# class UserLoginView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         if email and password:
#             user = get_user_model().objects.filter(email=email).first()

#             if user and user.check_password(password):
#                 token, created = Token.objects.get_or_create(user=user)
#                 return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)

#         return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
#     def get(self, request, *args, **kwargs):
#         # GET 요청에 대한 응답 추가
#         return Response({'detail': 'GET method is not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# class UserLogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         request.auth.delete()
#         return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)

# class UserPasswordChangeView(PasswordChangeView):
#     template_name = 'registration/password_change_form.html'
#     success_url = reverse_lazy('password_change_done')
#     permission_classes = [IsAuthenticated]

# from rest_framework.response import Response
# from rest_framework.decorators import api_view

# from .models import User
# from fishbread.models import Fishbread
# # from .serializers import UserSerializer
# from fishbread.serializers import FishbreadSerializer

# from django.shortcuts import get_object_or_404

# # Create your views here.
# @api_view(['GET', 'POST'])
# def fishbread_info(request):

#     if request.method == 'GET':
#         fishbreads = Fishbread.objects.all()
#         serializer = FishbreadSerializer(fishbreads, many=True)
#         return Response(data=serializer.data)
    
#     if request.method == 'POST':
#         serializer = FishbreadSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(data=serializer.data)

# @api_view(['GET', 'POST'])
# def fishbread_detail(request, id):
#     user = get_object_or_404(User, user_id=id)

#     if request.method == 'GET':
#         fishbreads = Fishbread.objects.filter(user_id=user)
#         serializer = FishbreadSerializer(fishbreads, many=True)
#         return Response(data=serializer.data)
    
#     elif request.method == 'POST':
#         serializer = FishbreadSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data)
