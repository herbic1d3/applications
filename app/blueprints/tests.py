import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from keys.models import Key
from blueprints.models import Blueprint


class TestBlueprintsAccess(TestCase):

    def setUp(self):
        user = get_user_model()
        self.user = user.objects.create_superuser(
            username='super',
            email='super@u.com',
            password='qwerty',
        )
        self.key = Key.objects.create()
        Blueprint.objects.create(title='test1', key=self.key)
        Blueprint.objects.create(title='test2', key=self.key)

    def test_unauthenticated_test_access(self):
        """
        Test unauthenticated access to /api/test/
        :return:
        """
        response = self.client.get(reverse('api_test-detail', args=(self.key.id, )))
        self.assertEqual(response.status_code, 401)

    def test_authenticated_access(self):
        response = self.client.post(reverse("api-token-auth"), data={
            "username": "super",
            "password": "qwerty",
        })
        self.assertEqual(response.status_code, 200)

    def test_authenticated_test_access(self):
        response = self.client.post(reverse("api-token-auth"), data={
            "username": "super",
            "password": "qwerty",
        })
        self.assertEqual(response.status_code, 200)

        self.client.defaults['HTTP_AUTHORIZATION'] = "Token {}".format(response.data.get("token"))
        response = self.client.get(reverse('api_test-detail', args=(self.key.id,)))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)


class TestBlueprintsMethods(TestCase):

    def setUp(self):
        user = get_user_model()
        self.user = user.objects.create_superuser(
            username='super',
            email='super@u.com',
            password='qwerty',
        )
        self.key = Key.objects.create()
        self.blueprint = Blueprint.objects.create(title='test1', key=self.key)
        Blueprint.objects.create(title='test2', key=self.key)
        Blueprint.objects.create(title='test3', key=self.key)
        Blueprint.objects.create(title='test4', key=Key.objects.create())

        response = self.client.post(reverse("api-token-auth"), data={
            "username": "super",
            "password": "qwerty",
        })
        self.client.defaults['HTTP_AUTHORIZATION'] = "Token {}".format(response.data.get("token"))

    def test_create_blueprint(self):
        response = self.client.post(reverse("api_blueprint-list"), data={
            'key': self.key.id,
            'title': 'test create'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Blueprint.objects.count(), 5)

    def test_update(self):
        old_title = self.blueprint.title
        new_title = 'test update'
        response = self.client.put(reverse('api_blueprint-detail', args=(self.blueprint.id, )),
                data = {'key': self.key.id, 'title': new_title},
                content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        blueprint = Blueprint.objects.get(pk=self.blueprint.id)
        self.assertEqual(self.blueprint.id, blueprint.id)
        self.assertEqual(blueprint.title, new_title)

    def test_update_wrong_key(self):
        response = self.client.put(reverse('api_blueprint-detail', args=(self.blueprint.id, )),
                data = {'key': uuid.uuid4(), 'title': 'test update'},
                content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_destroy(self):
        blueprint_count = Blueprint.objects.count()
        response = self.client.delete(reverse('api_blueprint-detail', args=(self.blueprint.id, )),
                data = {'key': self.key.id},
                content_type='application/json'
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Blueprint.objects.count()+1, blueprint_count)
