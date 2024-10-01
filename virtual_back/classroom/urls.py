from django.urls import path
from . import views
from django.urls import include, path
from rest_framework import routers

from tutorial.quickstart import views
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('check-enrollment/<int:class_id>/', views.check_enrollment, name='check_enrollment'),
    path('enroll/<int:class_id>/', views.enroll_in_class, name='enroll_in_class'),
    path('class-content/<int:class_id>/', views.get_class_content, name='get_class_content'),
    path('user-classes/', views.get_user_classes, name='get_user_classes'),
    path('upcoming-sessions/', views.get_upcoming_sessions, name='get_upcoming_sessions'),
    path('recent-activities/', views.get_recent_activities, name='get_recent_activities'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    # Add views for classes, units, sessions, lectures, etc.
]
