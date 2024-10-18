from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from booking_services_app.models import User, Appointment
from booking_services_app.serializers import UserSerializer, AppointmentSerializer


@api_view(['POST'])
def create_user(request):
    global serializer
    if request.method == 'POST':
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_users(request):
    global serializer
    if request.method == 'GET':
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e.add_note("User Not Found") , status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_appointments(request):
    if request.method == 'GET':
        try:
            appointments = Appointment.objects.all()
            serializer = AppointmentSerializer(appointments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e.add_note("Appointment Not Found") , status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user(request, id):
    global serializer
    if request.method == 'GET':
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

"""
@api_view(['POST'])
def create_appointment(request):
    global serializer
    if request.method == 'POST':
        try:
            serializer = AppointmentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            """


        # check ID and user type being passed when creating appointment
        # if user type is not service provider then inform the user that the id is not a service provider
        # create end points for updating info, deleting etc

"""
@api_view(['POST'])
def create_appointment1(request):
    if request.method == 'POST':
        service_provider_id = request.data.get('appointment_service_provider')
        try:
            serializer = AppointmentSerializer(data=request.data)
            if serializer.is_valid():
                id = serializer.validated_data.get('id')

                try:
                    user = User.objects.get(service_provider_id=service_provider_id)
                except User.DoesNotExist:
                    return Response({'Error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

                if user.user_type != 'service_provider':
                    return Response({'Error': 'The provided user ID does not belong to a service provider'}, status=status.HTTP_400_BAD_REQUEST)

                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'Error': 'Error'}, status=status.HTTP_400_BAD_REQUEST)
"""


"""
api_view(['POST'])
def create_appointment(request):
    service_provider_id = request.data.get('service_provider')

    try:
        service_provider = User.objects.get(pk=service_provider_id, user_type='service_provider')

        appointment_data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'dates': request.data.get('dates'),
            'service_provider': service_provider.id,
            'price': request.data.get('price': request.data.get('price')),
            'location': request.data.get('location'),
            'duration': request.data.get('duration'),
        }
        serializer = AppointmentSerializer(data=appointment_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response({"error": "Service provider not found or invalid"}, status=status.HTTP_400_BAD_REQUEST)
"""

@api_view(['POST'])
def create_appointment1(request):
    service_provider_id = request.data.get('appointment_service_provider')

    try:
        service_provider = User.objects.get(pk=service_provider_id, user_type='service_provider')

        appointment_data = {
            'appointment_name': request.data.get('appointment_name'),
            'appointment_description': request.data.get('appointment_description'),
            'appointment_date': request.data.get('appointment_date'),
            'appointment_service_provider': service_provider.id,
            'appointment_price': request.data.get('appointment_price'),
            'appointment_location': request.data.get('appointment_location'),
            'appointment_duration': request.data.get('appointment_duration'),
        }

        serializer = AppointmentSerializer(data=appointment_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response({"error": "Service provider not found or invalid"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def update_appointment(request):
    if request.method == 'PATCH':
        data = request.data
        appointment = Appointment.objects.get(id=data['id'])
        serializer = AppointmentSerializer(appointment, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_appointment(request, id):
    if request.method == 'DELETE':
        try:
            appointment = Appointment.objects.get(id=id)
            appointment.delete()
            return Response({"message": f" Appointment Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Appointment.DoesNotExist:
            return Response({"message": f"Appointment Not Found"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def book_appointment(request, appointment_id):
    if request.method == 'POST':
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response({"message": f"Appointment Not Found"}, status=status.HTTP_400_BAD_REQUEST)
        consumer = request.data.get('appointment_consumer')
        if not consumer:
            return Response({"error": "Only Consumers can Book Appointments"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(service_provider_id=appointment.service_provider_id, user_type='consumer')
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        appointment.appointment_consumer.add(consumer)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)