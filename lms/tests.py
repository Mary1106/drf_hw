from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from lms.models import Course, Lesson, Subscription
from users.models import User


class CourseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.test')
        self.course = Course.objects.create(title='Тестовый курс', description='Описание', owner=self.user)
        self.lesson = Lesson.objects.create(title='Тестовый урок', course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse('lms:course-detail', args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), self.course.title)

    def test_course_create(self):
        url = reverse('lms:course-list')
        data = {
            "title": "Тестовый курс2",
            "description": "Описание тестового курса2"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update(self):
        url = reverse('lms:course-detail', args=(self.course.pk,))
        data = {
            "title": "Тестовый курс2 upd"
        }
        response = self.client.patch(url, data)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('title'), 'Тестовый курс2 upd')

    def test_course_delete(self):
        url = reverse('lms:course-detail', args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        url = reverse('lms:course-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results":[
                {
                    "id": self.course.pk,
                    "title": self.course.title,
                    "preview": self.course.preview,
                    "description": self.course.description,
                    "lessons_in_course_count": 1
                }
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.test')
        self.course = Course.objects.create(title='Тестовый курс', description='Описание', owner=self.user)
        self.lesson = Lesson.objects.create(title='Тестовый урок', course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('lms:lesson_retrieve', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(data.get('title'), self.lesson.title)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_create(self):
        url = reverse('lms:lesson_create')
        data = {
            "title": "Тестовое создание урока",
            "course": self.course.pk,
            "video_url": "https://www.youtube.com"
        }
        response = self.client.post(url, data)
        print(f"URL: {url}")
        print(f"Data: {data}")
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.json()}")
        self.assertEqual(Lesson.objects.all().count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_update(self):
        url = reverse('lms:lesson_update', args=(self.lesson.pk,))
        data = {
            "title": "Патченый урок"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Патченый урок")

    def test_lesson_delete(self):
        url = reverse("lms:lesson_destroy", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("lms:lesson_list")
        response = self.client.get(url)
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "title": self.lesson.title,
                    "video_url": None,
                    "preview": None,
                    "course": self.course.pk,
                    "owner": self.user.pk
                }
            ]
        }
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class SubscriptionTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.test')
        self.course = Course.objects.create(title='Тестовый курс', description='Описание', owner=self.user)
        self.lesson = Lesson.objects.create(title='Тестовый урок', course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)
        
    def test_subscription(self):
        url = reverse('lms:subscription')
        data = {
            "user": self.user.pk,
            "course_id": self.course.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], "Подписка добавлена")

