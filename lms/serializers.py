from rest_framework import serializers
from lms.models import Course, Lesson, Subscription
from lms.validators import validate_links


class CourseSerializer(serializers.ModelSerializer):
    lessons_in_course_count = serializers.SerializerMethodField()
    title = serializers.CharField(validators=[validate_links])
    description = serializers.CharField(validators=[validate_links])

    def get_lessons_in_course_count(self, object):
        return object.lessons.count()

    class Meta:
        model = Course
        fields = ["id", "title", "preview", "description", "lessons_in_course_count"]


class LessonSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[validate_links])
    video_url = serializers.URLField(validators=[validate_links])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(read_only=True, many=True)
    lessons_in_course_count = serializers.SerializerMethodField()

    def get_lessons_in_course_count(self, object):
        return object.lessons.count()

    class Meta:
        model = Course
        fields = ["id", "title", "preview", "description", "lessons_in_course_count", "lessons", "owner"]


class SubscriptionSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = "__all__"
