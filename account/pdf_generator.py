#
# from django.shortcuts import render
#
# from fpdf import FPDF
#
# # pdf = FPDF() or
# # pdf = FPDF(orientation="P", unit="mm", format="A4")
# # pdf.add_page()
# # pdf.set_font("helvetica", "B", 16)
# # pdf.cell(40, 10, "Hello World!")
# # pdf.output("tuto1.pdf")
#
#
# class PDF(FPDF):
#     def header(self):
#         # Rendering logo:
#         self.image("../docs/fpdf2-logo.png", 10, 8, 33)
#         # Setting font: helvetica bold 15
#         self.set_font("helvetica", "B", 15)
#         # Moving cursor to the right:
#         self.cell(80)
#         # Printing title:
#         self.cell(30, 10, "Title", border=1, align="C")
#         # Performing a line break:
#         self.ln(20)
#
#     def footer(self):
#         # Position cursor at 1.5 cm from bottom:
#         self.set_y(-15)
#         # Setting font: helvetica italic 8
#         self.set_font("helvetica", "I", 8)
#         # Printing page number:
#         self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")
#
#
# # Instantiation of inherited class
# pdf = PDF()
# pdf.add_page()
# pdf.set_font("Times", size=12)
# for i in range(1, 41):
#     pdf.cell(0, 10, f"Printing line number {i}", new_x="LMARGIN", new_y="NEXT")
# pdf.output("new-tuto2.pdf")

from django.shortcuts import render
from django.http import FileResponse
from fpdf import FPDF


def index(request):
    context = {}
    return render(request, "account/index.html", context=context)


def report(request):
    result = [
        {"item": "Keyboard", "amount": "$120,00"},
        {"item": "Mouse", "amount": "$10,00"},
        {"item": "House", "amount": "$1 000 000,00"},
    ]
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('courier', 'B', 16)
    pdf.cell(40, 10, 'This is what you have sold this month so far:',0,1)
    pdf.cell(40, 10, '',0,1)
    pdf.set_font('courier', '', 12)
    pdf.cell(200, 8, f"{'Item'.ljust(30)} {'Amount'.rjust(20)}", 0, 1)
    pdf.line(10, 30, 150, 30)
    pdf.line(10, 38, 150, 38)
    for line in result:
        pdf.cell(200, 8, f"{line['item'].ljust(30)} "
                         f"{line['amount'].rjust(20)}",
                 0, 1)
    pdf.output('report.pdf', 'F')
    return FileResponse(open('report.pdf', 'rb'), as_attachment=True, content_type='application/pdf')