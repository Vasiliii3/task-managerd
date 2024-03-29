from django.urls import reverse
from task_manager.users.models import CustomUser
from task_manager.statuses.models import Status
from django.test import TestCase, Client
from http import HTTPStatus


class StatussTest(TestCase):
    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        self.client = Client()
        self.user1 = CustomUser.objects.get(pk=1)
        self.client.force_login(self.user1)
        self.status1 = Status.objects.get(pk=1)
        self.home = reverse('statuses_home')
        self.new_status = reverse('statuses_create')
        self.login_url = reverse('users_login')
        self.name = 'статустест'
        self.status_data = {
            'name': self.name,
        }

    def test_status_access_page(self):
        response = self.client.get(self.home)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.client.logout()
        response = self.client.get(self.home)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.login_url)

    def test_status_creature(self):
        response = self.client.post(self.new_status, data=self.status_data, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        test_statuss = Status.objects.last()
        self.assertEqual(test_statuss.name, self.name)

    def test_status_update(self):
        url = reverse('statuses_update', args=[self.status1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.post(url, self.status_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        updated_Status = Status.objects.get(id=self.status1.id)
        self.assertEqual(updated_Status.name, self.name)

    def test_status_delete(self):
        url = reverse('statuses_delete', args=[self.status1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        with self.assertRaises(Status.DoesNotExist):
            Status.objects.get(id=self.status1.id)
