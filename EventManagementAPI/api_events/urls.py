from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, TicketViewSet, RegisterView, TopEventsByTicketsSold, top_selling_events, CustomTokenObtainPairView,CustomTokenRefreshView

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'tickets', TicketViewSet)

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/', include(router.urls)),
    path('api/top-events/', TopEventsByTicketsSold.as_view(), name='top-events-by-tickets-sold'),
    path('api/events/top-selling/', top_selling_events, name='top_selling_events'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),

]