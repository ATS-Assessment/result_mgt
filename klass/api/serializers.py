
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from account.models import User
from result.models import Result
from ..models import Klass, Subject


class KlassCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Klass
        exclude = ("created_at",)

    # def create(self, validated_data):
    #     klass = Klass.objects.create(**validated_data)

    def update(self, instance, validated_data):
        user = self.context.get("request").user
        # instance.

        return instance


class SubjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("name", "level")


class SubjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "role", "username", "full_name")


class EducatorDashBoardSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()
    teacher = TeacherSerializer(read_only=True)

    class Meta:
        model = Klass
        fields = "__all__"

    def get_result(self, obj):
        return ResultSerializer(Result.objects.filter(classes=Klass.objects.get(teacher=obj.teacher)), many=True).data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class TeacherDetailSerializer(serializers.ModelSerializer):
    teacher = UserSerializer()

    class Meta:
        model = Klass
        exclude = ("created_at",)

    # def create(self, validated_data):
    #     klass = Klass.objects.create(**validated_data)

    def update(self, instance, validated_data):
        user = self.context.get("request").user
        # instance.

        return instance


class ClassCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Klass
        fields = "__all__"
        extra_kwargs = {
            'previous_teachers': {'read_only': True},
            'created_at': {'read_only': True},
        }

    def create(self, validated_data):
        subjects = validated_data.pop("subjects", [])
        klass = Klass.objects.create(**validated_data)
        klass.subjects = subjects
        klass.save()

        return klass

    def validate(self, attrs):
        name = attrs.get("name")
        teacher = attrs.get("teacher")
        klass_does_exist = Klass.objects.filter(name=name).exists()
        if klass_does_exist:
            raise serializers.ValidationError(
                "A klass with this name already exists")
        teacher_is_assigned = Klass.objects.filter(
            teacher__full_name=teacher).exists()
        if teacher_is_assigned:
            raise serializers.ValidationError(
                "This Teacher is already assigned to a Class")
        return attrs


class ClassDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Klass
        fields = "__all__"


class AdminEditClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Klass
        fields = ("name", "subjects", "session", "year", "teacher")


class EducatorEditClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Klass
        fields = ("name", "subjects", "session", "year", )
