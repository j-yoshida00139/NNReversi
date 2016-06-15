import json
from django.http import Http404, HttpResponse

def test(request):
    if request.is_ajax() and request.method == 'POST':
        todo_items = ['Mow Lawn', 'Buy Groceries',]
        data = json.dumps(todo_items)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

def add_todo(request):
    if request.is_ajax() and request.POST:
        data = {'message': "%s added" % request.POST.get('item')}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404