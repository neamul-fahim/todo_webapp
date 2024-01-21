from django.shortcuts import render, get_object_or_404
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TodoModelSerializer
from .models import Todo
from django.conf import settings
from .forms import TodoForm
from django.contrib.auth import get_user_model, authenticate, login

User = get_user_model()


# Create your views here.
class SignupPageView(View):
    template_name = 'todo/signup.html'

    def get(self, request, *args, **kwargs):
        context = {
            'BASE_API_URL': settings.BASE_API_URL,
        }
        return render(request, self.template_name, context)


class LoginPageView(View):
    template_name = 'todo/login.html'

    def get(self, request, *args, **kwargs):
        context = {
            'BASE_API_URL': settings.BASE_API_URL,
        }
        return render(request, self.template_name, context)


class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get("username", None)
        password = request.data.get("password", None)
        if username == None or password == None:
            return Response("username or password can't be null", status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(
            request=request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response('Login successful', status=status.HTTP_200_OK)
        else:
            return Response('Invalid credentials', status=status.HTTP_400_BAD_REQUEST)


class HomePageView(View):
    template_name = 'todo/home_page.html'

    def get(self, request, *args, **kwargs):
        context = {
            'BASE_API_URL': settings.BASE_API_URL,
        }
        return render(request, self.template_name, context)


class CreateTodoView(View):
    template_name = 'todo/post.html'

    def get(self, request, *args, **kwargs):
        form = TodoForm()
        context = {
            'BASE_API_URL': settings.BASE_API_URL,
            'form': form
        }
        return render(request, self.template_name, context)


class UpdateTodoView(View):
    template_name = 'todo/update_todo.html'

    def get(self, request, *args, **kwargs):

        context = {
            'BASE_API_URL': settings.BASE_API_URL,
        }
        return render(request, self.template_name, context)


class CreateUserAPIView(APIView):
    def post(self, request):
        username = request.data.get("username", None)
        password = request.data.get("password", None)
        if username == None or password == None:
            return Response("username or password can't be null", status=status.HTTP_400_BAD_REQUEST)

        existing_user = User.objects.filter(username=username).first()
        if existing_user is not None:
            return Response("User already exists", status=status.HTTP_400_BAD_REQUEST)

        try:
            User.objects.create_user(username=username, password=password)
            return Response("user created", status=status.HTTP_200_OK)
        except:
            return Response("something went wrong", status=status.HTTP_400_BAD_REQUEST)


class GetTodoAPIView(APIView):

    def get(self, request, todo_id):
        todo = get_object_or_404(Todo, id=todo_id)
        serializer = TodoModelSerializer(todo)
        # print(f"-------article-------{serializer.data}")
        return Response(serializer.data)


class TodoAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        # Sort by created_at in descending order
        todos = Todo.objects.filter(user=user).order_by('-created_at')
        serializer = TodoModelSerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        form = TodoForm(request.data)
        print(
            f"----------------------create todo--------{request.data}---------")

        if form.is_valid():
            # Create a Todo instance but don't save it yet
            todo_instance = form.save(commit=False)
            # Set any additional fields or manipulate the instance if needed
            # For example, you can set the user who created the todo
            print(f"----------------------create todo-----------------")
            print(
                f"----------------------create todo-----{self.request.user}-----")
            todo_instance.user = self.request.user  # Assuming you have user authentication
            # Save the Todo instance
            todo_instance.save()

            serializer = TodoModelSerializer(todo_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        todo_id = pk

        if not todo_id:
            return Response({'error': 'Todo ID is required for deletion.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            todo = Todo.objects.get(id=todo_id)
            todo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Todo.DoesNotExist:
            return Response({'error': 'Todo not found.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, *args, **kwargs):
        todo = get_object_or_404(Todo, pk=pk, user=self.request.user)
        print(f"-------------update----------{todo}")
        serializer = TodoModelSerializer(instance=todo, data=request.data)
        print(f"-------------update-------------")

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
