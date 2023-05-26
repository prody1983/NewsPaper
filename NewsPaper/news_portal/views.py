from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


class PostsList(LoginRequiredMixin, ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-time_create'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 2  # вот так мы можем указать количество записей на странице

   # Переопределяем функцию получения списка новостей
    def get_queryset(self):
       # Получаем обычный запрос
       queryset = super().get_queryset()

       # Используем наш класс фильтрации.
       # self.request.GET содержит объект QueryDict, который мы рассматривали
       # в этом юните ранее.
       # Сохраняем нашу фильтрацию в объекте класса,
       # чтобы потом добавить в контекст и использовать в шаблоне.
       self.filterset = PostFilter(self.request.GET, queryset)

       # Возвращаем из функции отфильтрованный список новостей
       return self.filterset.qs
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)

       # Добавляем в контекст объект фильтрации.
       context['filterset'] = self.filterset
       context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()

       return context

class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельной статье
    model = Post
    # Используем другой шаблон — post.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранная статья
    context_object_name = 'post'

# Добавляем новое представление для создания статьи.
class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news_portal.add_post',)

    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        # признак статьи
        post.a_or_n = 1
        return super().form_valid(form)


# Добавляем новое представление для создания новости.
class NewsCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        # признак новости
        post.a_or_n = 0
        return super().form_valid(form)

# Добавляем представление для изменения статьи.
class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news_portal.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

# Представление удаляющее статью.
class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('post_list')

class CategoryListView(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'category_list.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'category_news_list'
    paginate_by = 2  # вот так мы можем указать количество записей на странице

   # Переопределяем функцию получения списка новостей
    def get_queryset(self):
        self.categories = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categories=self.categories).order_by('-time_create')
        return queryset

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)

       # Добавляем в контекст переменные.
       context['is_not_subscriber'] = self.request.user not in self.categories.subscribers.all()
       context['category'] = self.categories

       return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})


