from django.shortcuts import redirect, render, get_object_or_404
from vagas.forms import VagasForm
from .models import Vaga
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from vagas.forms import RegisterUpdateForm
from vagas.forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .utils.recommendation import gerar_recomendacoes


# Create your views here.
def index(request):
    return render(request, "vagas/index.html")


def search(request):
    search_value = request.GET.get("q", "").strip()

    if search_value == "":
        return redirect("index")

    # A busca nas tags deve ser feita dessa forma
    vagas = Vaga.objects.filter(
        Q(title__icontains=search_value)
        | Q(salary__icontains=search_value)
        | Q(location__icontains=search_value)
        | Q(company_name__icontains=search_value)
        | Q(tags__name__icontains=search_value)  # Busca nas tags associadas
    ).distinct()  # Garantir que as vagas não se repitam

    context = {
        "vagas": vagas,
    }

    return render(request, "vagas/vagas.html", context=context)


@login_required(login_url="register")
def create(request):

    if request.method == "POST":
        form = VagasForm(request.POST)
        context = {"form": form}

        if form.is_valid():
            vaga = form.save(commit=False)
            vaga.owner = request.user
            vaga.save()
            return redirect("vagas")

        return render(request, "vagas/create.html", context=context)

    context = {"form": VagasForm()}
    return render(request, "vagas/create.html", context=context)


def vagas(request):

    vagas = Vaga.objects.all().order_by("-date_created")

    return render(request, "vagas/vagas.html", {"vagas": vagas})


def register(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("vagas")

    context = {
        "form": form,
    }

    return render(request, "vagas/registerForm.html", context=context)


def login_view(request):
    form = AuthenticationForm(request)

    if request.method == "POST":

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect("index")

    context = {
        "form": form,
    }

    return render(request, "vagas/login.html", context=context)


def logout_view(request):
    auth.logout(request)
    return redirect("login")


@login_required(login_url="register")
def user_update(request):

    form = RegisterUpdateForm(instance=request.user)

    if request.method != "POST":
        return render(request, "vagas/user_update.html", {"form": form})

    form = RegisterUpdateForm(data=request.POST, instance=request.user)

    if not form.is_valid():
        return render(request, "user_update.html", {"form": form})

    form.save()
    return redirect("vagas")


@login_required(login_url="register")
def vaga(request, vaga_id):

    vaga = Vaga.objects.get(pk=vaga_id)

    context = {
        "vaga": vaga,
    }

    return render(request, "vagas/vaga.html", context=context)


@login_required(login_url="register")
def delete(request, vaga_id):
    vaga = Vaga.objects.get(pk=vaga_id)
    vaga.delete()
    return redirect("vagas")



#--------------------------------------------------
#--------------------------------------------------

def detalhe_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    recomendacoes = gerar_recomendacoes(vaga_id)

    # Debugging
    print("Vaga:", vaga)
    print("Recomendações:", recomendacoes)

    return render(request, 'vagas/vaga.html', {
        'vaga': vaga,
        'recomendacoes': recomendacoes
    })
