from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import taskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request, "home.html")

#creando el usuario
def signup(request):

    if request.method == "GET":
        return render(request, "signup.html", {
            "form": UserCreationForm
        })

    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST["password1"])
                # guardamos el usuario en la base de datos
                user.save()
                # guardamos la cookie de sesion
                login(request, user)
                return redirect("tasks")

            except IntegrityError:
                return render(request, "signup.html", {
                    "form": UserCreationForm,
                    "error": "Usuario already exist"
                })

        return render(request, "signup.html", {
            "form": UserCreationForm,
            "error": "contrasenas no coinciden"
        })

@login_required
def tasks(request):
    #mostrando los datos del usuario logueado
    task = Task.objects.filter(user=request.user,datecompleted__isnull=True)
    return render(request, "tasks.html",{
        "tasks":task
    })


@login_required
def tasks_completed(request):
    #mostrando los datos del usuario logueado
    task = Task.objects.filter(user=request.user,datecompleted__isnull=False).order_by("-datecompleted")
    return render(request, "tasks.html",{
        "tasks":task
    })


@login_required
def create_task(request):


    if request.method == "GET":
        return render(request,"create_task.html",{
        "form":taskForm
    })
    else:
        #guardando las tareas
        try:
            form = taskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        
        except ValueError:
            return render(request,"create_task.html",{
                "form":taskForm,
                "error":"Por favor utilize datos validos"
            })
        

@login_required
def task_detail(request,task_id:int):
    if request.method == "GET":
        task = get_object_or_404(Task,pk=task_id,user = request.user)
        form = taskForm(instance=task)
        return render(request,"task_detail.html",{
            "tasks":task,
            "form":form
        })
    else:
        #Actualizando las tareas
        try:
            task = get_object_or_404(Task,pk=task_id,user=request.user)
            form = taskForm(request.POST, instance=task)
            form.save()

            return redirect("tasks")
        
        except ValueError:
            return render(request,"task_detail.html",{
            "tasks":task,
            "form":form,
            "error":"Error actualizando la tarea"
        })

@login_required
def complete_task(request,task_id):
    task = get_object_or_404(Task,pk=task_id,user=request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect("tasks")

@login_required
def delete_task(request,task_id):
    task = get_object_or_404(Task,pk=task_id,user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("tasks")


# cerrando la sesion
@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {
            "form": AuthenticationForm
        })
    else:
        #confirmando si el usuario y contrasena existen
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        #si no existen se redirecciona al formulario con un error
        if user is None:
            return render(request, "signin.html", {
            "form": AuthenticationForm,
            "error":"Username or password is incorrect"
        })
        #El usuario existe y guardamos la sesion
        else:
            #guardamos la sesion
            login(request,user)
            return redirect("tasks")
        

        
