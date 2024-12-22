from django.urls import path

from app.views import ChatbotView, LoginView, LogoutView, SignupView, UploadDocumentView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("upload-document/", UploadDocumentView.as_view(), name="upload_document"),
    path("", ChatbotView.as_view(), name="chatbot"),
]
