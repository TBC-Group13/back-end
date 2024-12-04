from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'created_at', 'status']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['repeat_password']:
            raise serializers.ValidationError({"repeat_password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('repeat_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class UserSerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()
    answers_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'reputation', 'bio',
            'location', 'website', 'date_joined', 'questions_count',
            'answers_count'
        ]
        read_only_fields = ['reputation']

    def get_questions_count(self, obj):
        return obj.questions.count()

    def get_answers_count(self, obj):
        return obj.answers.count()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'created_at', 'status', 'profile_photo']
