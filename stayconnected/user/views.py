from django.contrib.auth.password_validation import validate_password
from django.contrib.messages.storage import default_storage
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Sum, F
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.parsers import MultiPartParser, FormParser
from .models import User
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer, UserProfileSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'Registration successful',
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserLoginView(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request):
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             password = serializer.validated_data['password']
#             user = authenticate(email=email, password=password)
#
#             if user is not None:
#                 refresh = RefreshToken.for_user(user)
#                 return Response({
#                     'tokens': {
#                         'refresh': str(refresh),
#                         'access': str(refresh.access_token),
#                     },
#                     'user': {
#                         'id': user.id,
#                         'username': user.username,
#                         'email': user.email
#                     }
#                 })
#             return Response({'error': 'Invalid credentials'},
#                             status=status.HTTP_401_UNAUTHORIZED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            identifier = serializer.validated_data['identifier']
            password = serializer.validated_data['password']

            # First, try to find the user by either username or email
            try:
                if '@' in identifier:
                    user = User.objects.get(email=identifier)
                else:
                    user = User.objects.get(username=identifier)

                # Check password
                if user.check_password(password):
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'tokens': {
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                        },
                        'user': {
                            'id': user.id,
                            'username': user.username,
                            'email': user.email
                        }
                    })
                else:
                    return Response({'error': 'Invalid credentials'},
                                    status=status.HTTP_401_UNAUTHORIZED)

            except User.DoesNotExist:
                return Response({'error': 'Invalid credentials'},
                                status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({'error': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

            # Blacklist the token
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'message': 'Logged out successfully.'}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({'error': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        if user.profile_photo:
            user.profile_photo.delete()
            user.profile_photo = None
            user.save()
            return Response({"message": "Profile photo removed."}, status=status.HTTP_200_OK)
        return Response({"error": "No profile photo to remove."}, status=status.HTTP_400_BAD_REQUEST)


class UserSettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        data = request.data
        if 'username' in data:
            new_username = data['username']
            if User.objects.exclude(pk=user.pk).filter(username=new_username).exists():
                return Response(
                    {'username': 'This username is already taken.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.username = new_username

        if 'email' in data:
            new_email = data['email']
            if User.objects.exclude(pk=user.pk).filter(email=new_email).exists():
                return Response(
                    {'email': 'This email is already in use.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.email = new_email

        if 'profile_photo' in data:
            if user.profile_photo:
                default_storage.delete(user.profile_photo.path)  # this correct?

            user.profile_photo = data['profile_photo']

        if 'password' in data:
            new_password = data['password']

            try:
                validate_password(new_password, user)
            except ValidationError as e:
                return Response(
                    {'password': list(e.messages)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.set_password(new_password)
        try:
            user.full_clean()
            user.save()
        except ValidationError as e:
            return Response(
                {'detail': e.message_dict},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserReputationAPIView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        likes_count = user.like_count
        dislikes_count = user.dislike_count
        accepted_count = user.accepted_count

        # Calculate reputation to look more like stackoverflow
        reputation = 10 * likes_count - 5 * dislikes_count + 15 * accepted_count

        return Response({
            "user_id": user_id,
            "likes": likes_count,
            "dislikes": dislikes_count,
            "reputation": reputation,
            "answers_count": user.answers.count(),
            "accepted_answers": user.accepted_count,
        })


class UserReputationListAPIView(APIView):
    def get(self, request):
        ordering = request.query_params.get('ordering', '-reputation_score')
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))

        users = User.objects.annotate(
            reputation_score=F('like_count') * 10 - F('dislike_count') * 5 + F('accepted_count') * 15
        )

        users = users.order_by(ordering)
        paginator = Paginator(users, page_size)

        try:
            page_obj = paginator.page(page)
        except EmptyPage:
            return Response({
                'error': 'Page not found',
                'total_pages': paginator.num_pages
            }, status=status.HTTP_404_NOT_FOUND)

        user_data = []
        for user in page_obj:
            user_data.append({
                "user_id": user.id,
                "username": user.username,
                "reputation_score": user.reputation_score,
                "likes": user.like_count,
                "dislikes": user.dislike_count,
                "answers_count": user.answers.count(),
                "accepted_answers": user.accepted_count,
            })

        return Response({
            'users': user_data,
            'total_users': paginator.count,
            'total_pages': paginator.num_pages,
            'current_page': page,
            'page_size': page_size,
        })