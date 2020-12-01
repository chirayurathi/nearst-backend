from django.http import HttpResponse
from django.views.generic import View
from .utils import render_to_pdf
from datetime import date
from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def GeneratePdf(request):
    print('this',request.body.decode('utf-8'))
    data = json.loads(request.body.decode('utf-8'))
    data['today'] = date.today()
    pdf = render_to_pdf('pdf/invoice.html', data)
    response = HttpResponse(pdf, content_type='application/pdf')
    # response['Access-Control-Allow-Origin'] = '*'
    # response['Access-Control-Allow-Headers'] = 'content-type, Access-Control-Allow-Origin'
    return response