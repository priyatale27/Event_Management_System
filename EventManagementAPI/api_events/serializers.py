from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Event, Ticket
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        user.role = validated_data.get('role', 'User')
        user.save()
        return user


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'date', 'total_tickets', 'tickets_sold']

    def validate(self, data):
        if data['total_tickets'] < 0:
            raise serializers.ValidationError("Total tickets must be a positive integer.")
        if data['tickets_sold'] < 0:
            raise serializers.ValidationError("Tickets sold cannot be negative.")
        return data


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'user', 'event', 'quantity', 'purchase_date']

    def validate(self, data):
        if data['quantity'] <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return data