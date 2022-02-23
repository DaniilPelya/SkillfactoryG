from django_filters import FilterSet, DateFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post
import django.forms


# создаём фильтр
class PostFilter(FilterSet):
    time_in_post = DateFilter(
        lookup_expr='gt',
        widget=django.forms.DateInput(
            attrs={
                'type': 'date',
            }
        )
    )
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т. е. подбираться) информация о товарах
    class Meta:
        model = Post
        fields = {'title_post': ['icontains'],
                  'author': ['in'],
        }  # поля, которые мы будем фильтровать (т. е. отбирать по каким-то критериям, имена берутся из моделей)