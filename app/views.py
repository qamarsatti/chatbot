import json

from django import http
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from app.forms import CustomUserCreationForm, DocumentUploadForm
from app.models import Document, PDFEmbedding
from app.utils import extract_text_from_pdf, generate_embeddings, query_chatbot


class SignupView(FormView):
    template_name = "signup.html"
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("chatbot")


class LoginView(FormView):
    template_name = "login.html"
    form_class = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect("/")


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")


class UploadDocumentView(LoginRequiredMixin, FormView):
    template_name = "upload_document.html"
    form_class = DocumentUploadForm

    def form_valid(self, form):
        try:
            pdf_file = form.cleaned_data["document"]

            document = Document.objects.create(
                user=self.request.user, title=pdf_file.name
            )
            text = extract_text_from_pdf(pdf_file)
            chunks = [text[i : i + 500] for i in range(0, len(text), 500)]
            for chunk in chunks:
                embedding = generate_embeddings(chunk)
                PDFEmbedding.objects.create(
                    text=chunk,
                    embedding=embedding,
                    user=self.request.user,
                    document=document,
                )
            return redirect("chatbot")
        except Exception as e:
            return http.HttpResponseBadRequest("Error" + str(e))


class DocumentDeleteView(LoginRequiredMixin, View):
    """
    A view that deletes all documents for the current logged-in user.
    """

    def post(self, request, *args, **kwargs):

        Document.objects.filter(user=request.user).delete()
        PDFEmbedding.objects.filter(user=request.user).delete()
        return redirect("chatbot")


class ChatbotView(LoginRequiredMixin, TemplateView):
    template_name = "chatbot.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["documents"] = Document.objects.filter(user=self.request.user)
        return context

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        query = data.get("query")
        answer = query_chatbot(query, self.request.user)
        return JsonResponse({"response": answer})
