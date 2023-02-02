from cuentas.models import SolicitudAsociacionAgencia
from django.shortcuts import get_object_or_404, render
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.http.response import HttpResponseRedirect
from django.urls import reverse


from .forms import  TuristaSignUpForm, SolicitudIngresoAgenciaForm, FormularioDeSolicitudMuestra
from agencias.models import User


class TuristatSignUpView(CreateView):
    model = User
    form_class = TuristaSignUpForm
    template_name = 'signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'turista'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('turista-home')


def solicitud_agencia(request):
    if request.method=="POST":
        form = SolicitudIngresoAgenciaForm(request.POST)
        if form.is_valid():
            solicitud =  form.save()
            return HttpResponseRedirect(reverse('solicitud-validada', args=(solicitud.IdS,)))
    else:
        form = SolicitudIngresoAgenciaForm()
    return render(request, 'agencia_solicitud.html', {'form': form})

def solicitud_validada(request, pk):
    #sol = get_object_or_404(SolicitudAsociacionAgencia, pk=pk)
    #form = FormularioDeSolicitudMuestra(solicitud=sol)
    return render(request, 'solicitud_validada.html')#, {'form':form})