from django_ajax.decorators import ajax
from .models import Tag


@ajax
def update_tags(request):
    current_tags = Tag.objects.filter(slug__icontains=request.POST['text']).order_by('favor_set')
    return {'msg': current_tags[0:10]}