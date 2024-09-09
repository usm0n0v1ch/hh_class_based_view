from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.shortcuts import get_object_or_404, redirect

from app.models import Vacancy, Resume, Response
from app.forms import ResumeForm, VacancyForm


class VacancyListView(ListView):
    model = Vacancy
    template_name = 'app/vacancy_list.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        return Vacancy.objects.filter(title__icontains=search_query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_responses'] = Response.objects.filter(user=self.request.user).values_list('vacancy_id', flat=True)
        return context


class VacancyDetailView(DetailView):
    model = Vacancy
    template_name = 'app/vacancy_detail.html'
    context_object_name = 'vacancy'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_responded'] = Response.objects.filter(user=self.request.user, vacancy=self.object).exists()
        return context



class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'app/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes'] = Resume.objects.filter(user=self.request.user)
        context['vacancies'] = Vacancy.objects.filter(user=self.request.user)
        return context


class ResumeCreateView(LoginRequiredMixin, CreateView):
    model = Resume
    form_class = ResumeForm
    template_name = 'app/resume_create.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ResumeDetailView(DetailView):
    model = Resume
    template_name = 'app/resume_detail.html'
    context_object_name = 'resume'



class ResumeEditView(LoginRequiredMixin, UpdateView):
    model = Resume
    form_class = ResumeForm
    template_name = 'app/resume_edit.html'
    success_url = reverse_lazy('profile')


# Resume Delete View
class ResumeDeleteView(LoginRequiredMixin, DeleteView):
    model = Resume
    template_name = 'app/resume_confirm_delete.html'
    success_url = reverse_lazy('profile')



class ResumeListView(LoginRequiredMixin, ListView):
    template_name = 'app/resume_list.html'
    context_object_name = 'resumes'

    def get_queryset(self):

        return Resume.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancies = Vacancy.objects.filter(user=self.request.user)
        responses = Response.objects.filter(vacancy__in=vacancies)
        context['vacancies'] = vacancies
        context['responses'] = responses
        return context


class VacancyCreateView(LoginRequiredMixin, CreateView):
    model = Vacancy
    form_class = VacancyForm
    template_name = 'app/vacancy_create.html'
    success_url = reverse_lazy('profile')



class RespondToVacancyView(LoginRequiredMixin, DetailView):
    model = Vacancy
    template_name = 'app/vacancy_detail.html'

    def post(self, request, *args, **kwargs):
        vacancy = self.get_object()
        resume = Resume.objects.filter(user=request.user).first()

        if not resume:
            return redirect('resume_create')

        Response.objects.get_or_create(user=request.user, resume=resume, vacancy=vacancy)
        return redirect(reverse('vacancy_detail', kwargs={'pk': vacancy.id}))
