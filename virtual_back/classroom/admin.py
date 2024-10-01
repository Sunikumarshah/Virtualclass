from django.contrib import admin

# Register your models here.
# classroom/admin.py

from django.contrib import admin
from .models import Class, Enrollment, Session, Lecture, Comment

admin.site.register(Class)
admin.site.register(Enrollment)
admin.site.register(Session)
admin.site.register(Lecture)
admin.site.register(Comment)

