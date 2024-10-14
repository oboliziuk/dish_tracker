from django.test import TestCase
from django.urls import reverse
from dishops.models import DishType, Cook


class IndexViewTest(TestCase):
    def setUp(self):
        self.cook = Cook.objects.create_user(
            username="testuser", password="password123", years_of_experience=5
        )

    def test_index_view_with_login(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("dishops:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dishops/index.html")
        self.assertIn("num_cooks", response.context)
        self.assertIn("num_dishes", response.context)
        self.assertIn("num_dish_types", response.context)
        self.assertIn("num_visits", response.context)


class DishTypeListViewTest(TestCase):
    def setUp(self):
        self.cook = Cook.objects.create_user(
            username="testuser", password="password123", years_of_experience=5
        )
        DishType.objects.create(name="Appetizer")
        DishType.objects.create(name="Main Course")

    def test_dish_type_list_view_with_login(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("dishops:dish_type_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dishops/dish_type_list.html")
        self.assertEqual(len(response.context["dish_type_list"]), 2)

    def test_dish_type_search(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("dishops:dish_type_list"), {"name": "Appetizer"})
        self.assertEqual(len(response.context["dish_type_list"]), 1)
        self.assertContains(response, "Appetizer")
