from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from .models import Tag


@dajaxice_register
def suggest_tag(request, search):
    dajax = Dajax()
    matched_tags = Tag.objects.filter(headline__startswith=search)
    result = []
    for tag in matched_tags:
        result.append("<code>$s</code" % tag.slug)
    dajax.assign('#result', 'innerHTML', result)
    return dajax.json()


@dajaxice_register
def multiply(request, a, b):
    dajax = Dajax()
    result = int(a) * int(b)
    dajax.assign('#result','value',str(result))
    return dajax.json()