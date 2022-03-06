from django.forms import ModelForm
from .models import Post, Author, User
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


# Создаём модельную форму
class PostForm(ModelForm):
    # в класс мета, как обычно, надо написать модель, по которой будет строится форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        fields = ['title_post', 'article_or_news', 'category', 'text_post', 'author']


# Создаем форму для регистрации, авторизации и автоматического добавления нового пользователя в основную группу сайта,
# переопределив форму из allauth - SignupForm, а именно переопределив метод save()
class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)  # вызываем метод save() класса-родителя, чтобы необходимые проверки и сохранение в модель User были выполнены.
        common_group = Group.objects.get(name='common')  # получаем объект модели группы basic
        common_group.user_set.add(user)  # через атрибут user_set, возвращающий список всех пользователей этой группы, мы добавляем нового пользователя в эту группу
        return user  # Обязательным требованием метода save() является возвращение объекта модели User по итогу выполнения функции.


