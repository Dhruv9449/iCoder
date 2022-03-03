from django import template

register = template.Library()


@register.filter(name='not_reply')
def not_reply(comment):
    return comment.filter(parent=None)
