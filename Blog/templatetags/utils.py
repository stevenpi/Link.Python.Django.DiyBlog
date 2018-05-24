from django.template import Library
from vote.models import UP, DOWN

register = Library()


@register.filter
def user_has_voted(model_entity, user):
    if model_entity.votes.exists(user.id, action=UP):
        return True
    elif model_entity.votes.exists(user.id, action=DOWN):
        return True
    else:
        return False


@register.filter
def user_voted_up(model_entity, user):
    return model_entity.votes.exists(user.id, action=UP)


@register.filter
def user_voted_down(model_entity, user):
    return model_entity.votes.exists(user.id, action=DOWN)
