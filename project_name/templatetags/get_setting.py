# Based on the Stack Overflow answers provided here - http://stackoverflow.com/a/6343321 and
# here - http://stackoverflow.com/a/8462170.

from django.template import Library, Node, TemplateSyntaxError, Variable
from django.conf import settings

register = Library()


# [From the SO answer]
# I found some tricks in URLNode and url from defaulttags.py:
# https://code.djangoproject.com/browser/django/trunk/django/template/defaulttags.py
@register.tag
def get_setting(parser, token):
    as_value = variable = default = ''
    bits = token.split_contents()
    tag_name = bits[0]
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument "
                                  "(settings constant to retrieve)" % tag_name)

    variable = bits[1].strip('"\'')

    bits = bits[2:]
    if len(bits) >= 2 and bits[-2] == 'as':
        as_value = bits[-1]
        bits = bits[:-2]

    # The only thing that should be left is a default value.
    if len(bits) == 1:
        default = bits[0].strip('"\'')
    elif len(bits):
        raise TemplateSyntaxError("'%s' can't process the arguments '%s'"
                                  % (tag_name, ", ".join(bits)))

    return SettingNode(variable=variable, default=default, as_value=as_value)


class SettingNode(Node):
    def __init__(self, variable, default, as_value):
        self.variable = getattr(settings, variable, default)
        self.ctxname = as_value

    def render(self, context):
        if self.ctxname:
            context[self.ctxname] = self.variable
            return ''
        else:
            return self.variable
