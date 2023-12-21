from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from .forms import AnnouncementForm, ResponseForm, NewsForm
from .models import Announcement, Response


# Представление для отображения всех объявлений
class AnnouncementView(ListView):
    model = Announcement
    template_name = 'forum/index.html'
    context_object_name = 'posts'
    success_url = reverse_lazy('home')
    extra_context = {'title': 'Все объявления'}
    paginate_by = 3


# Представление для одного выбраного объявления
class DetailAnnouncementView(DetailView):
    model = Announcement
    template_name = 'forum/post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'announcement_id'


# Представление для добавления объявлений
class AddAnnouncement(LoginRequiredMixin, CreateView):
    form_class = AnnouncementForm
    template_name = 'forum/add_announcement.html'
    extra_context = {'title': 'Добавить Объявление'}

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        return super().form_valid(form)


# Редактирование объявлений. Редактировать может только автор (логика доступа в шаблоне 'post.html')
class UpdateAnnouncement(LoginRequiredMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'forum/add_announcement.html'
    extra_context = {'title': 'Редактировать Объявление'}


# Удаление объявлений. Удалять может только автор (логика доступа в шаблоне 'post.html')
class DeleteAnnouncement(LoginRequiredMixin, DeleteView):
    model = Announcement
    template_name = 'forum/post_delete.html'
    extra_context = {'title': 'Удалить Объявление'}
    success_url = reverse_lazy('home')


# Отправка отклика к объявлению
def add_response(request, pk):
    post = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            resp = form.save(commit=False)
            resp.announcement = post
            resp.author = request.user
            resp.save()

            # Отправка уведомления на почту автора объявления
            link = f'{settings.DOMAIN_NAME}/post/{post.pk}'
            login = f'{settings.DOMAIN_NAME}{reverse("users:login")}'
            subject = 'Вам оставили новый отклик'
            message = f'Необходимо авторизоваться - {login}; и перейти по ссылке - {link}'
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[post.author.email],
                fail_silently=False
            )
            return render(request, 'forum/index.html')

    else:
        form = ResponseForm()

    context = {'form': form, 'post': post}
    return render(request, 'forum/add_response.html', context)


# Представление для показа откликов и фильтрация по объявлениям
class ListResponseFilter(ListView):
    model = Response
    template_name = 'forum/list_response.html'
    context_object_name = 'responses'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Announcement.objects.get(pk=self.kwargs['announcement_id'])
        return context

    def get_queryset(self):
        return Response.objects.filter(announcement_id=self.kwargs['announcement_id'])


# Принятие отклика. Принимать может только автор объявления(логика доступа для автора в шаблоне 'list_response.html')
class AcceptResponse(UpdateView):
    model = Response
    fields = ['status']
    template_name = 'forum/add_response.html'
    extra_context = {'title': 'Принять отклик'}


# Отклонение отклика. Отклонять может только автор объявления(логика доступа для автора в шаблоне 'list_response.html')
class DeleteResponse(DeleteView):
    model = Response
    template_name = 'forum/delete_response.html'
    extra_context = {'title': 'Отклонить отклик?'}
    success_url = reverse_lazy('home')


class DetailResponse(DetailView):
    model = Response
    template_name = 'forum/response.html'
    context_object_name = 'response'


# Рассылка новостей всем пользователям. Отправлять может только admin (логика доступа в шаблоне '_nav.html')
def send_news_admin(request):
    users = get_user_model().objects.all()
    emails = [user.email for user in users if user.email]
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=emails,
                fail_silently=False
            )
            return redirect('send_news')
    else:
        form = NewsForm()

    return render(request, 'forum/send_news.html', {'form': form})






