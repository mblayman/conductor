from django import template

register = template.Library()


@register.filter()
def startswith(text: str, prefix: str) -> bool:
    """A wrapper for str.startswith.

    This is customized a bit to split on comma and return if anything matches.
    """
    if "," in prefix:
        return any([text.startswith(p) for p in prefix.split(",")])
    return text.startswith(prefix)
