from django.shortcuts import render
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets, serializers
from django.contrib.auth.models import User, Group
from .models import Class, Enrollment
# from .serializers import ClassSerializer, EnrollmentSerializer
from .models import Session, Comment
from .serializers import GroupSerializer, UserSerializer,RegisterSerializer,ChangePasswordSerialize





# views.py


@api_view(['GET'])
def check_enrollment(request, class_id):
    user = request.user
    try:
        classroom = Class.objects.get(id=class_id)
        if Enrollment.objects.filter(student=user, classroom=classroom).exists():
            return Response({"message": "Enrolled"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Not Enrolled"}, status=status.HTTP_403_FORBIDDEN)
    except Class.DoesNotExist:
        return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['student', 'classroom']
@api_view(['POST'])
def enroll_in_class(request, class_id):
    user = request.user
    try:
        classroom = Class.objects.get(id=class_id)
        Enrollment.objects.create(student=user, classroom=classroom)
        return Response({"message": "Successfully enrolled"}, status=status.HTTP_201_CREATED)
    except Class.DoesNotExist:
        return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)
# views.py

@api_view(['GET'])
def get_class_content(request, class_id):
    user = request.user
    try:
        classroom = Class.objects.get(id=class_id)
        if Enrollment.objects.filter(student=user, classroom=classroom).exists():
            # Return the class content here
            return Response({"class_content": "Your class content here"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Not enrolled"}, status=status.HTTP_403_FORBIDDEN)
    except Class.DoesNotExist:
        return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_user_classes(request):
    user = request.user
    if user.is_authenticated:
        # Get classes where user is either the instructor or enrolled
        instructed_classes = Class.objects.filter(instructor=user)
        enrolled_classes = Class.objects.filter(enrollments__student=user)

        # Prepare response
        classes = instructed_classes.union(enrolled_classes)
        class_data = [{"id": c.id, "name": c.name, "instructor_name": c.instructor.username} for c in classes]
        
        return Response(class_data, status=200)
    return Response({"error": "Not authenticated"}, status=403)

@api_view(['GET'])
def get_upcoming_sessions(request):
    user = request.user
    if user.is_authenticated:
        # Get upcoming sessions for the classes the user is enrolled in
        enrollments = Enrollment.objects.filter(student=user)
        sessions = Session.objects.filter(unit__classroom__in=enrollments.values_list('classroom_id', flat=True))
        
        session_data = [{"id": s.id, "title": s.title, "scheduled_time": s.scheduled_time} for s in sessions]
        
        return Response(session_data, status=200)
    return Response({"error": "Not authenticated"}, status=403)

@api_view(['GET'])
def get_recent_activities(request):
    user = request.user
    if user.is_authenticated:
        # Get recent comments or updates for the user's enrolled classes
        enrollments = Enrollment.objects.filter(student=user)
        activities = Comment.objects.filter(lecture__session__unit__classroom__in=enrollments.values_list('classroom_id', flat=True)).order_by('-created_at')[:10]
        
        activity_data = [{"id": a.id, "message": a.text, "timestamp": a.created_at} for a in activities]
        
        return Response(activity_data, status=200)
    return Response({"error": "Not authenticated"}, status=403)
