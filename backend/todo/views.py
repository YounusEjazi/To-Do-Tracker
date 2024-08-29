from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Todo
from .serializer import TodoSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class TodoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        todos = Todo.objects.filter(user=user)
        serializer = TodoSerializer(todos, many=True)
        return Response({
            'status': True,
            'data': serializer.data,
            'message': 'Todos fetched successfully'
        })

    def post(self, request):
        try:
            user = request.user
            data = request.data.copy()  # Create a copy of the request data to modify it
            data['user'] = user.id  # Use user.id or user.pk instead of user.uid
            serializer = TodoSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Invalid fields',
                    'data': serializer.errors
                })

            serializer.save()
            return Response({
                'status': True,
                'message': 'Todo created successfully',
                'data': serializer.data
            })

        except Exception as e:
            return Response({
                'status': False,
                'message': 'Something went wrong: ' + str(e),
                'data': {}
            })

    def patch(self, request, uuid=None):
        try:
            user = request.user
            data = request.data
            if uuid is None:
                return Response({
                    'status': False,
                    'message': 'UUID is required',
                    'data': {}
                })

            obj = Todo.objects.filter(uuid=uuid, user=user)

            if not obj.exists():
                return Response({
                    'status': False,
                    'message': 'Invalid UUID',
                    'data': {}
                })

            serializer = TodoSerializer(obj[0], data=data, partial=True)

            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Invalid fields',
                    'data': serializer.errors
                })

            serializer.save()
            return Response({
                'status': True,
                'message': 'Todo updated successfully',
                'data': serializer.data
            })

        except Exception as e:
            return Response({
                'status': False,
                'message': 'Something went wrong: ' + str(e),
                'data': {}
            })
