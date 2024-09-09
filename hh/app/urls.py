from django.urls import path
from app import views

urlpatterns = [
    path('vacancy_list/', views.VacancyListView.as_view(), name='vacancy_list'),
    path('vacancy_detail/<int:pk>/', views.VacancyDetailView.as_view(), name='vacancy_detail'),
    path('resume_create/', views.ResumeCreateView.as_view(), name='resume_create'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('resume_detail/<int:pk>/', views.ResumeDetailView.as_view(), name='resume_detail'),
    path('resume_edit/<int:pk>/', views.ResumeEditView.as_view(), name='resume_edit'),
    path('resume_delete/<int:pk>/', views.ResumeDeleteView.as_view(), name='resume_delete'),
    path('resume_list/', views.ResumeListView.as_view(), name='resume_list'),
    path('vacancy_create/', views.VacancyCreateView.as_view(), name='vacancy_create'),
    path('vacancy/<int:pk>/respond/', views.RespondToVacancyView.as_view(), name='respond_to_vacancy'),
]
