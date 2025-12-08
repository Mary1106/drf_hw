from rest_framework.serializers import ModelSerializer, SerializerMethodField
from lms.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    lessons_in_course_count = SerializerMethodField()

    def get_lessons_in_course_count(self, object):
        return object.lessons.count()

    class Meta:
        model = Course
        fields = ["title", "preview", "description", "lessons_in_course_count"]


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    lessons = LessonSerializer(read_only=True, many=True)
    lessons_in_course_count = SerializerMethodField()

    def get_lessons_in_course_count(self, object):
        return object.lessons.count()

    class Meta:
        model = Course
        fields = ["title", "preview", "description", "lessons_in_course_count", "lessons"]
