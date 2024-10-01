from rest_framework import serializers
from django.contrib.auth.models import Group, User
from .models import Class, Enrollment, Session, Comment
from rest_framework.validators import UniqueValidator  # Correct import
from django.contrib.auth.password_validation import validate_password  # Correct password validation import


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_instructor']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]  # Use the imported UniqueValidator
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])  # Correct validator
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ClassSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.username', read_only=True)

    class Meta:
        model = Class
        fields = ['id', 'name', 'instructor_name']


class EnrollmentSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.username', read_only=True)
    class_obj_name = serializers.CharField(source='class_obj.name', read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'student_username', 'class_obj', 'class_obj_name']


# Add other serializers as needed, e.g., SessionSerializer, CommentSerializer
class SessionSerializer(serializers.ModelSerializer):
    class_obj_name = serializers.CharField(source='unit.class_obj.name', read_only=True)

    class Meta:
        model = Session
        fields = ['id', 'title', 'scheduled_time', 'unit', 'class_obj_name']


class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'lecture', 'user', 'user_username', 'text', 'parent', 'replies', 'created_at']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []
