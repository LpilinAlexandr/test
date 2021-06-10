from django.shortcuts import render, resolve_url
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound
from .forms import EmailForm, ApiForm


def email_view(request):
    """
    Форма для получения электронной почты
    """
    form = EmailForm()
    if request.method == 'POST':
        form = EmailForm(request=request,
                         url=resolve_url(to='email'),
                         data=request.POST)
        if form.is_valid():
            response_text = form.save()
            return HttpResponse(response_text)
        else:
            return HttpResponse(form.errors.as_json(), status=400)

    return render(request, 'main/email.html', {
        'form': form
    })


@csrf_exempt
def api_view(request):
    """
    Страница для API запросов
    """
    if request.method == 'POST':
        # По заданию на метод POST ищем в GET параметрах method и логируем параметры
        form = ApiForm(params=request.GET,
                       url=resolve_url(to='api'),
                       request=request)
        if form.is_valid():
            response_text = form.save()
            return HttpResponse(response_text)
        else:
            errors = form.errors.as_json()
            return HttpResponse(errors, status=400)

    # По заданию на метод GET, а за одно и на всё остальное отвечаем 404
    return HttpResponse('Bad request', status=404)
