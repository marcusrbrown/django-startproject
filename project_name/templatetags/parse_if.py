# Loosely based on noparse.py from https://code.djangoproject.com/ticket/14502

from django import template
from django.template.defaulttags import TemplateIfParser

register = template.Library()

token_formats = {
    template.TOKEN_TEXT: u'%s',
    template.TOKEN_VAR: u'%s%%s%s' % (template.VARIABLE_TAG_START, template.VARIABLE_TAG_END),
    template.TOKEN_COMMENT: u'%s%%s%s' % (template.COMMENT_TAG_START, template.COMMENT_TAG_END),
    # template.TOKEN_BLOCK is handled in place; formatting breaks on '%}'.
}


@register.tag
def parse_if(parser, token):
    bits = token.split_contents()
    tag_name = bits[0]
    end_tag = 'end%s' % tag_name
    condition = TemplateIfParser(parser, bits[1:]).parse()
    text = []
    while parser.tokens:
        token = parser.next_token()
        if (token.token_type == template.TOKEN_BLOCK) and (token.contents == end_tag):
            return ParseIfNode(condition, u''.join(text))
        if token.token_type == template.TOKEN_BLOCK:
            text.append(u'%s%s%s' % (template.BLOCK_TAG_START, token.contents,
                                     template.BLOCK_TAG_END))
        else:
            text.append(token_formats[token.token_type] % token.contents)
    parser.unclosed_block_tag(end_tag)


class ParseIfNode(template.Node):
    def __init__(self, condition, text):
        self.condition = condition
        self.text = text

    def render(self, context):
        try:
            match = self.condition.eval(context)
        except template.VariableDoesNotExist:
            match = None

        if match:
            return self._render(context)

        return ''

    def _render(self, context):
        # Instantiating a Template object uses a new Parser instance, so
        # none of the loaded libraries carry over. Each new Parser instance
        # imports builtin libraries by default. Since we can't access the
        # Parser instance created to parse the template, we temporarily add
        # a library to builtins that contains all of the libraries that are
        # currently loaded.  A better way to do this would be a mechanism
        # to override the Parser instance (or compile_string() function)
        # used in the new Template.
        temp_lib = self._aggregate_libraries(template.libraries.values())
        builtins = template.builtins
        builtins.append(temp_lib)
        cursor = builtins.index(temp_lib)
        try:
            return template.Template(self.text).render(context)
        finally:
            # Remove our temporary library from builtins, so that it
            # doesn't pollute other parsers.
            del builtins[cursor]

    def _aggregate_libraries(self, libraries):
        temp_lib = template.Library()
        for library in libraries:
            temp_lib.tags.update(library.tags)
            temp_lib.filters.update(library.filters)
        return temp_lib
