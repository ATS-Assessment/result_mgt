
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import IsAdminUser
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives, EmailMessage
from xhtml2pdf import pisa
from html import escape
import io
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import login, logout, authenticate
from account.models import User
from klass.api.permissions import IsEducator, IsEducatorOrReadOnly
from result.models import Result, Score,  Token
from ..models import Klass, Subject

from .serializers import KlassCreateSerializer, \
    AdminEditClassSerializer, EducatorEditClassSerializer,\
    ClassDetailSerializer, ClassCreateSerializer,\
    SubjectCreateSerializer, EducatorDashBoardSerializer, \
    ResultListSerializer, ResultCreateSerializer, ScoreListSerializer, SubjectListSerializer
from .renderers import CustomRenderer


class KlassCreateAV(generics.CreateAPIView):
    serializer_class = KlassCreateSerializer
    queryset = Klass.objects.all()
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class KlassUpdateAV(generics.UpdateAPIView):
    serializer_class = KlassCreateSerializer
    queryset = Klass.objects.all()
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class SubjectCreateAV(generics.CreateAPIView):
    serializer_class = SubjectCreateSerializer
    queryset = Subject.objects.all()
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class AdminSubjectListAV(generics.ListAPIView):
    serializer_class = SubjectCreateSerializer
    queryset = Subject.objects.all()
    permission_classes = [IsAdminUser]
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class DeleteSubjectView(APIView):
    serializer_class = SubjectListSerializer
    permission_classes = [IsAdminUser]
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

    def get(self, request, pk, *args, **kwargs):
        try:
            get_obj = Subject.objects.get(pk=pk)
            get_obj.is_active = not (get_obj.is_active)

            get_obj.save()
            return Response({"message": f"{get_obj.name} was successfully deactivated!"}, status=status.HTTP_204_NO_CONTENT)
        except Subject.DoesNotExist as e:
            return Response({"message": f"{get_obj.name} deactivation failed! or {e} "}, status=status.HTTP_400_BAD_REQUEST)


class EducatorDashBoardAV(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EducatorDashBoardSerializer
    queryset = Result.objects.all()
    permission_classes = [IsEducator]
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

    def get_queryset(self):
        return super().get_queryset().filter(
            classes=Klass.objects.get(teacher=self.request.user))

    def retrieve(self, request, *args, **kwargs):
        klass = Klass.objects.get(teacher=request.user)
        serializer = self.serializer_class(klass)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClassDetailAV(generics.RetrieveUpdateDestroyAPIView):
    queryset = Klass.objects.all()
    serializer_class = ClassDetailSerializer
    permission_classes = [IsAuthenticated, IsEducator]
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class TeacherDetailAV(APIView):
    serializer_class = KlassCreateSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

    def get(self, request):
        klass = Klass.objects.get(teacher=request.user.id)
        serializer = self.serializer_class(klass)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClassCreateAV(generics.CreateAPIView):
    serializer_class = ClassCreateSerializer
    queryset = Klass.objects.all()
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


def render_to_pdf(template_src, context_dict):
    html = render_to_string(template_src, context_dict)
    result = io.BytesIO()

    pdf = pisa.pisaDocument(io.BytesIO(html.encode(
        "ISO-8859-1")), dest=result, encoding="ISO-8859-1")
    print(pdf, "Ok")
    if not pdf.err:
        return result.getvalue()
    return Response({"message": "We had some errors<pre>%s</pre>"}, status=status.HTTP_200_OK)


@ api_view(('GET',))
@ renderer_classes((CustomRenderer, JSONRenderer))
def generate_pdf(request, pk):
    result = Result.objects.get(pk=pk)
    # context = {
    #     "results": Score.objects.filter(result__pk=pk),
    #     "info": result
    # }
    pdf = render_to_pdf(
        'klass/result_details.html',
        {
            'pagesize': 'A4',
            "results": Score.objects.filter(result__pk=pk),
            "info": result
        }

    )
    print("Here", pdf)
    mail_address = [result.guardian_email]
    from_email = settings.DEFAULT_FROM_EMAIL
    subject = "Termly Result Of your Ward"
    message = "Dear Sir/Madam, Please find attached is a copy of your wards result for this term(in PDF format). We appreciate your trust and confidence in our capacities and capabilities to train and nurture your ward. We can't wait to welcome them back next term! Have an amazing holiday and Happy Halloween in Advance!."

    email_message = EmailMessage(
        subject, message, to=mail_address, from_email=from_email)
    filename = 'Result.pdf'
    mimetype_pdf = 'application/pdf'
    email_message.attach(filename, pdf, mimetype_pdf)
    email_message.send(fail_silently=False)  #

    messages.success(
        request, f"Result has been successfully sent to the parent/guardian's email!")
    return Response({"message": "Result was sent successfully", "data": pdf}, status=status.HTTP_200_OK)


def toggle_delete_result(request, pk):
    result = Result.objects.get(pk=pk)
    result.is_inactive = not result.is_inactive
    return Response({"message": "Result was successfully deleted"}, status=status.HTTP_204_NO_CONTENT)


class AdminEditClassAV(generics.RetrieveUpdateAPIView):
    queryset = Klass.objects.all()
    serializer_class = AdminEditClassSerializer
    # permission_classes = [IsAdminUser]
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

    def perform_update(self, serializer):
        klass = Klass.objects.get(pk=self.kwargs.get("pk"))
        # subjects = serializer.validated_data.get("subjects")
        # for subject in subjects:
        #     klass.subjects.append(subject)

        if klass.teacher.full_name != serializer.validated_data.get("teacher"):
            teacher_dict = {
                'name': klass.teacher.full_name,
                'session': klass.session
            }
            pre_teacher = [klass.previous_teachers].append(teacher_dict)

            klass.previous_teachers = pre_teacher

        check_teacher = Klass.objects.filter(
            teacher__full_name=serializer.validated_data.get("teacher"))
        if check_teacher:
            raise ValidationError(
                "The Teacher has already been assigned to a class")
        klass.save()


class EducatorEditClassAV(generics.RetrieveUpdateAPIView):
    queryset = Klass.objects.all()
    serializer_class = EducatorEditClassSerializer


class ResultAPIView(ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultListSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    permission_classes = [IsEducatorOrReadOnly]


class AddResultAPIView(generics.CreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultCreateSerializer
    permission_classes = (IsAuthenticated,)


class StudentResultAPIView(generics.RetrieveUpdateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultListSerializer

    def get(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            admission_num = request.data.get('admission_number')
            student_token = request.data.get('token')
            academic_session = request.data.get('session')
            academic_term = request.data.get('term')

            token = Token.objects.get(token=student_token)


class ResultScoresAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreListSerializer
    permission_classes = (IsAuthenticated,)
