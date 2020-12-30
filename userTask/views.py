from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AllTasksSerializer
from .models import UserTask


@api_view(['GET', 'POST', 'DELETE'])
def allTasks(request):
    if request.method == 'GET':
        allTasks = request.user.task.all()
        print("hello", allTasks)
        serializer = AllTasksSerializer(request.user.task.all(), many=True )
        return Response(serializer.data)
    
    elif request.method =="POST":
        user = request.user
        task = UserTask(user=user)
        serializer = AllTasksSerializer(task, data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            # new_serializer = AllTasksSerializer(request.user.task.all(), many=True )
            # return Response(new_serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method =="DELETE":
        user = request.user
        id = request.GET.get('id')
        print(id)
        task = UserTask.objects.get(id=id).delete()
        serializer = AllTasksSerializer(task, data=request.data)
        print(request.data)
        if task:
            new_serializer = AllTasksSerializer(request.user.task.all(), many=True )
            return Response(new_serializer.data, status=status.HTTP_201_CREATED)
        else:
            data={"failed":"Deletion Failed"}
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

