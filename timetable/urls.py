from django.urls import path
from .views import fetch_latest_timetable, check_timetable_version, upload_timetable

urlpatterns = [
    path('api/timetable/latest/', fetch_latest_timetable, name='fetch_latest_timetable'),
    path('api/timetable/version/', check_timetable_version, name='check_timetable_version'),
    path('api/timetable/upload/', upload_timetable, name='upload_timetable'),
]