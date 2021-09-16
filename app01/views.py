
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from xhtml2pdf.default import DEFAULT_FONT

from io import BytesIO
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import render_to_string

from .models import CourseRecord

pdfmetrics.registerFont(TTFont('yh', 'static/font/msyh.ttf' ))
DEFAULT_FONT['helvetica'] = 'yh'

def print_record(request):
    record_id = request.GET.get('record_id')
    obj = CourseRecord.objects.get(id=record_id)
    if obj.state!=2:
        return HttpResponse('上课记录必须签到才能打印')
    params = {
        'pagesize':'A4',
        'obj': obj,
        'shopName':'heijinjulebu'
    }

    from django.shortcuts import render

    # return render(request, 'webprint3.html', params)

    html = render_to_string('webprint4.html', params).encode('utf-8')
    print(html)


    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html), result, encoding='UTF-8')
    converted = result.getvalue() if not pdf.err else ''

    filename = 'Questionario-di-gradimento.pdf'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    response.write(converted)
    return response