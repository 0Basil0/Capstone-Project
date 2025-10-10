from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
from .models import ChatHistory, Allergy

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def custom_logout(request):
    logout(request)
    return redirect('login')

@login_required
def base(request):
    return render (request, 'base.html')
@login_required
def home(request):
    return render (request, 'home.html')
class chatView(LoginRequiredMixin, ListView):
    model = ChatHistory
    
    template_name = 'chat_form.html'
    context_object_name = 'chats'
    
    def get_queryset(self):
        return ChatHistory.objects.filter(user=self.request.user).order_by('-timestamp')
# class ChatDetailView(LoginRequiredMixin, DetailView):
#     model = ChatHistory
#     template_name = 'chat_detail.html'
#     context_object_name = 'chat'
class AllergyListView(LoginRequiredMixin, ListView):
    model = Allergy
    
    template_name = 'allergies_form.html'
    context_object_name = 'allergies'
    def get_queryset(self):
        return Allergy.objects.filter(user=self.request.user)
