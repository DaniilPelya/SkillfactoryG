from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, \
    TemplateView  # импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД,
                                                       # импортируем класс получения деталей объекта
from .models import Post, Category
from .forms import PostForm  # импортируем нашу форму
from .filters import PostFilter  # импортируем недавно написанный фильтр
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


# Create your views here.

class PostList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'posts.html'  # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'posts'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    # queryset = Post.objects.order_by('-id')  # если нужно выводить список queryset от более новых объектов к более старым
    ordering = ['-id']
    paginate_by = 10  # поставим постраничный вывод в один элемент
    # form_class = PostForm  # добавляем форм класс, чтобы получать доступ к форме через метод POST

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()  # добавили логическую переменную, которая дает True, если пользователя еще нет в авторах
        #context['categories'] = Category.objects.all()
        #context['form'] = PostForm()
        return context


    # def post(self, request, *args, **kwargs):
    #    form = self.form_class(request.POST)
    #
    #    if form.is_valid():
    #        form.save()
    #
    #    return super().get(request, *args, **kwargs)  # отправляем пользователя обратно на GET-запрос.

# создаём представление, в котором будут детали конкретного отдельного товара
class PostDetail(DetailView):
    # model = Post  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    # template_name = 'post.html'  # название шаблона будет post.html
    # context_object_name = 'post'  # название объекта в нём будет post
    template_name = 'post.html'
    queryset = Post.objects.all()


# дженерик для создания объекта. Надо указать только имя шаблона и класс формы, который мы написали в прошлом юните. Остальное он сделает за вас
class PostCreateView(PermissionRequiredMixin, CreateView):  # PermissionRequiredMixin миксин для проверки прав доступа
    permission_required = ('news.add_post',)
    template_name = 'post_create.html'
    form_class = PostForm


# дженерик для редактирования объекта
class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'post_create.html'
    form_class = PostForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class PostListSearch(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'posts_search.html'  # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'posts'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    # queryset = Post.objects.order_by('-id')  # если нужно выводить список queryset от более новых объектов к более старым
    ordering = ['-id']
    paginate_by = 10  # поставим постраничный вывод в один элемент
    # form_class = PostForm  # добавляем форм класс, чтобы получать доступ к форме через метод POST

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        #context['categories'] = Category.objects.all()
        #context['form'] = PostForm()
        return context


@login_required
def upgrade_me(request):  # функция-представление для добавления юсера в группу авторов, @login_required проверяет, зарегестрирован ли пользователь на сайте
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/news')



