from django.urls import path
from .views import PostList, PostDetail, PostCreateView, PostUpdateView, PostDeleteView, PostListSearch  # импортируем наше представление


urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно, почему
    path('', PostList.as_view()),  # т. к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('<int:pk>/', PostDetail.as_view(), name='post'),  # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    path('create/', PostCreateView.as_view(), name='post_create'),  # Ссылка на создание товара
    path('create/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('search/', PostListSearch.as_view(), name='posts_search'),  # путь к странице поиска постов
]
