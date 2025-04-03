# todo/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Todo
from .serializer import TodoSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

class TodoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        todos = Todo.objects.filter(user=user).order_by('-is_pinned', 'due_date')
        serializer = TodoSerializer(todos, many=True)
        logger.debug(f"GET todos for {user.username}: {serializer.data}")
        return Response({
            'status': True,
            'data': serializer.data,
            'message': 'Todos fetched successfully'
        })

    def post(self, request):
        try:
            user = request.user
            serializer = TodoSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save(user=user)  # ✅ Set user directly here
                return Response({
                    'status': True,
                    'message': 'Todo created successfully',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)

            return Response({
                'status': False,
                'message': 'Invalid fields',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"POST ERROR {str(e)}")
            return Response({
                'status': False,
                'message': 'Something went wrong: ' + str(e),
                'data': {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, uuid=None):
        try:
            user = request.user
            if not uuid:
                return Response({'status': False, 'message': 'UUID required'}, status=400)

            todo = Todo.objects.filter(uuid=uuid, user=user).first()
            if not todo:
                return Response({'status': False, 'message': 'Todo not found'}, status=404)

            serializer = TodoSerializer(todo, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': True,
                    'message': 'Todo updated successfully',
                    'data': serializer.data
                })

            return Response({'status': False, 'data': serializer.errors}, status=400)

        except Exception as e:
            logger.error(f"PATCH ERROR {str(e)}")
            return Response({
                'status': False,
                'message': 'Something went wrong: ' + str(e),
                'data': {}
            }, status=500)

    def delete(self, request, uuid=None):
        try:
            user = request.user
            if not uuid:
                return Response({
                    'status': False,
                    'message': 'UUID is required'
                }, status=status.HTTP_400_BAD_REQUEST)

            todo = Todo.objects.filter(uuid=uuid, user=user).first()
            if not todo:
                return Response({
                    'status': False,
                    'message': 'Todo not found or access denied'
                }, status=status.HTTP_404_NOT_FOUND)

            todo.delete()
            return Response({
                'status': True,
                'message': 'Todo deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            logger.error(f"DELETE ERROR: {str(e)}")
            return Response({
                'status': False,
                'message': 'Something went wrong: ' + str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
