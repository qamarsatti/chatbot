from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from app.forms import CustomUserCreationForm, DocumentUploadForm
from app.models import Document


class SignupView(FormView):
    template_name = "signup.html"
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("upload_document")


class LoginView(FormView):
    template_name = "login.html"
    form_class = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect("chatbot")


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")


class UploadDocumentView(LoginRequiredMixin, FormView):
    template_name = "upload_document.html"
    form_class = DocumentUploadForm

    def form_valid(self, form):
        uploaded_file = form.cleaned_data["document"]
        document_name = uploaded_file.name

        # Save the document name to the database
        Document.objects.create(user=self.request.user, document_name=document_name)
        return redirect("chatbot")


class ChatbotView(LoginRequiredMixin, TemplateView):
    template_name = "chatbot.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["documents"] = Document.objects.filter(user=self.request.user)
        return context
