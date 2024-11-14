from django.shortcuts import redirect, render
from vagas.forms import VagasForm
from .models import Vaga
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from vagas.forms import RegisterUpdateForm
from vagas.forms import RegisterForm



# Create your views here.
def index(request):
    return render(request, "vagas/index.html")


def create(request):

    if request.method == "POST":

        form = VagasForm(request.POST)

        context = {"form": form}

        if form.is_valid():
            form.save()
            return redirect("vagas")

        return render(request, "vagas/create.html", context=context)

    context = {"form": VagasForm()}

    return render(request, "vagas/create.html", context=context)


def vagas(request):

    vagas = Vaga.objects.all().order_by('-date_created')

    return render(request, "vagas/vagas.html", {"vagas": vagas})


def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()

    context = {
        'form': form,
    }

    return render(request, 'vagas/registerForm.html', context=context)


def login_view(request):
    form = AuthenticationForm(request)

    if request.method == 'POST':

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect('index')

    context = {
        'form': form,
    }

    return render(
        request,
        'vagas/login.html',
        context=context
    )

def logout_view(request):
    auth.logout(request)
    return redirect('login')


def user_update(request):

    
    
    form = RegisterUpdateForm(instance=request.user)

    if request.method != 'POST':
        return render(
            request,
            'vagas/user_update.html',
            {
                'form': form
            }
        )

    form = RegisterUpdateForm(data=request.POST, instance=request.user)

    if not form.is_valid():
        return render(
            request,
            'user_update.html',
            {
                'form': form
            }
        )

    form.save()
    return redirect('user_update')


def vaga(request, vaga_id):

    vaga = Vaga.objects.get(pk=vaga_id)

    context = {
        'vaga': vaga,
    }

    return render(
        request,
        'vagas/vaga.html',
        context=context
    )