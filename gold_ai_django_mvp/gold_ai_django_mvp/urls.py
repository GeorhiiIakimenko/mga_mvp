"""
URL configuration for gold_ai_django_mvp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# gold_ai_django_mvp/urls.py
from django.contrib import admin
from django.urls import path, include
from analysis_app.views import expert_opinion_form, index, analysis_page, chat_with_assistant, start_page

urlpatterns = [
    path('', start_page, name='start_page'),
    path('admin/', admin.site.urls),
    path('analysis/', include('analysis_app.urls')),
    path('expert_opinion/', expert_opinion_form, name='expert_opinion_form'),
    path('analysis_page/', analysis_page, name='analysis_page'),
    path('chat-with-assistant/', chat_with_assistant, name='chat_with_assistant'),
    path('index/', index, name='index'),
    # Добавьте другие URL-адреса по мере необходимости
]


