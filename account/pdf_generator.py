from django.shortcuts import render
from django.http import FileResponse
from fpdf import FPDF

from result.models import Result


def index(request):
    context = {}
    return render(request, "account/index.html", context=context)


def result_view(request):
    # student_id = request.POST.get('admission_number')
    # result = Result.objects.filter(resul_admission_number=student_id)
    # student_id = 'BA123353'
    result = [
        {"item": "Keyboard", "amount": "$120,00"},
        {"item": "Mouse", "amount": "$10,00"},
        {"item": "House", "amount": "$1 000 000,00"},
    ]
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('courier', 'B', 16)
    pdf.cell(40, 10, 'This is what you have sold this month so far:', 0, 1)
    pdf.cell(40, 10, '', 0, 1)
    pdf.set_font('courier', '', 12)
    pdf.cell(200, 8, f"{'Item'.ljust(30)} {'Amount'.rjust(20)}", 0, 1)
    pdf.line(10, 30, 150, 30)
    pdf.line(10, 38, 150, 38)
    for line in result:
        pdf.cell(300, 8, f"{line['item'].ljust(30)} "
                         f"{line['amount'].rjust(20)}"
                         f"{line['amount']}"
                         f"{line['amount']}"
                         f"{line['amount']}",
                 0, 1)
    pdf.output(f'result.pdf', 'F')
    return FileResponse(open('report.pdf', 'rb'),
                        as_attachment=True, content_type='application/pdf')
