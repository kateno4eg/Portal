from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value):
    censor_words = ['блядь', 'пиздец', 'жопа']
    for c in censor_words:
        value = value.replace(c, '(CENSORED)')
    return value