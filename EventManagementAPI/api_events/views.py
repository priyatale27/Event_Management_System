from rest_framework import generics, status, serializers
from django.contrib.auth.models import User
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, EventSerializer, TicketSerializer
from rest_framework import viewsets, permissions
from .models import Event, Ticket
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        if self.request.user.role == 'Admin':
            serializer.save()
        else:
            raise permissions.PermissionDenied("You don't have permission to create an event.")

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def purchase_ticket(self, request, pk=None):
        try:
            event = Event.objects.get(id=pk)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

        quantity = request.data.get('quantity')
        if not quantity or quantity <= 0:
            return Response({'error': 'Invalid quantity'}, status=status.HTTP_400_BAD_REQUEST)

        if event.tickets_sold + quantity > event.total_tickets:
            return Response(
                {'error': 'Not enough tickets available. Requested quantity exceeds available tickets.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        ticket = Ticket.objects.create(user=request.user, event=event, quantity=quantity)

        event.tickets_sold += quantity
        event.save()

        return Response(TicketSerializer(ticket).data, status=status.HTTP_201_CREATED)

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def perform_create(self, serializer):
        event = serializer.validated_data['event']
        if event.tickets_sold + serializer.validated_data['quantity'] <= event.total_tickets:
            serializer.save()
            event.tickets_sold += serializer.validated_data['quantity']
            event.save()
        else:
            raise serializers.ValidationError("Not enough tickets available.")


class TopEventsByTicketsSold(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = """
            SELECT 
                e.id, 
                e.name, 
                e.date, 
                e.total_tickets, 
                COALESCE(SUM(t.quantity), 0) AS total_tickets_sold
            FROM 
                events_event e
            LEFT JOIN 
                events_ticket t ON e.id = t.event_id
            GROUP BY 
                e.id
            ORDER BY 
                total_tickets_sold DESC
            LIMIT 3;
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        top_events = []
        for row in results:
            event = {
                'id': row[0],
                'name': row[1],
                'date': row[2],
                'total_tickets': row[3],
                'total_tickets_sold': row[4]
            }
            top_events.append(event)

        return Response(top_events, status=status.HTTP_200_OK)


@api_view(['GET'])
def top_selling_events(request):
    top_events = get_top_selling_events()
    return Response(top_events, status=status.HTTP_200_OK)


def get_top_selling_events():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, name, date, total_tickets, tickets_sold 
            FROM events_event 
            ORDER BY tickets_sold DESC 
            LIMIT 3;
        """)
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return results


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)

class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)