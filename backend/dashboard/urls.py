from django.urls import path
from .views import UserDashboardView, AdminAnalyticsView

urlpatterns = [
    path("me/", UserDashboardView.as_view(), name="user-dashboard"),
    path("admin-analytics/", AdminAnalyticsView.as_view(), name="admin-analytics"),
]
