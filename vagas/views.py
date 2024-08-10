from django.shortcuts import redirect, render
from vagas.forms import VagasForm
from .models import Vaga


# Create your views here.
def index(request):
    return render(request, "vagas/index.html")


def create(request):

    if request.method == "POST":

        form = VagasForm(request.POST)

        context = {"form": form}

        if form.is_valid():
            form.save()
            return redirect("create")

        return render(request, "vagas/create.html", context=context)

    context = {"form": VagasForm()}

    return render(request, "vagas/create.html", context=context)


def vagas(request):

    vagas = Vaga.objects.all()

    return render(request, "vagas/vagas.html", {"vagas": vagas})
