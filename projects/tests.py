from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from projects.models import Project

User = get_user_model()


class TeamFinderSimpleTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email="test1@yandex.ru",
            password="password123",
            name="Ivan",
            surname="Ivanov",
            phone="89991112233",
        )
        self.user2 = User.objects.create_user(
            email="test2@yandex.ru",
            password="password123",
            name="Petr",
            surname="Petrov",
            phone="89995556677",
        )

        self.project1 = Project.objects.create(
            name="Project One",
            description="First test project",
            owner=self.user1,
            status="open",
        )
        self.project1.participants.add(self.user1)

        self.project2 = Project.objects.create(
            name="Project Two",
            description="Second test project",
            owner=self.user2,
            status="open",
        )
        self.project2.participants.add(self.user2)

    def test_pages_availability(self):
        response = self.client.get(reverse("projects:project_list"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("users:participants_list"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("users:login"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("users:register"))
        self.assertEqual(response.status_code, 200)

    def test_project_creation(self):
        self.assertEqual(Project.objects.count(), 2)
        self.assertEqual(User.objects.count(), 2)

        self.assertEqual(self.project1.owner, self.user1)
        self.assertEqual(self.project2.owner, self.user2)
