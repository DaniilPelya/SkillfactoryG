from django import template
import re

register = template.Library()  # если мы не зарегистрируем наши фильтры, то Django никогда не узнает, где именно их искать и фильтры потеряются


@register.filter(name='censor')
def censor(value):
    mat = ['бляд', 'хуй', 'хуё', 'хуе', 'хуя', 'хую', 'пизд', 'еба', 'ебе', 'ебё', 'ёба']
    if isinstance(value, str):
        for el in mat:
            if el in value:
                value = value.replace(el, 'XXX')
        return value
    else:
        raise ValueError(f'филтр censor работает только со строками')
