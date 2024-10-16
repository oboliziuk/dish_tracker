from django.test import TestCase
from django.core.exceptions import ValidationError
from dishops.models import Dish, Cook, DishType
from dishops.forms import DishForm, CookCreationForm, CookExperienceUpdateForm, CookSearchForm, DishSearchForm, \
    DishTypeSearchForm


class DishFormTest(TestCase):
    def setUp(self):
        self.dish_type = DishType.objects.create(name="Main Course")
        self.cook = Cook.objects.create(username="chef", password="password")

    def test_valid_dish_form(self):
        form_data = {
            'name': 'Pasta',
            'description': 'Delicious pasta with sauce',
            'price': 12.99,
            'dish_type': self.dish_type.id,
            'cooks': [1],
        }
        form = DishForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_invalid_dish_form_empty_name(self):
        form_data = {
            'name': '',
            'description': 'Delicious pasta with sauce',
            'price': 12.99,
            'dish_type': '1',
            'cooks': [1],
        }
        form = DishForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)


class CookCreationFormTest(TestCase):
    def setUp(self):
        self.valid_form_data = {
            'username': 'chef123',
            'password1': 'SuperStrongPassword123',
            'password2': 'SuperStrongPassword123',
            'years_of_experience': 5,
            'first_name': 'John',
            'last_name': 'Doe',
        }

    def test_valid_cook_creation_form(self):
        form = CookCreationForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_invalid_years_of_experience(self):
        invalid_form_data = self.valid_form_data.copy()
        invalid_form_data['years_of_experience'] = 150

        form = CookCreationForm(data=invalid_form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('years_of_experience', form.errors)


class CookExperienceUpdateFormTest(TestCase):
    def test_valid_experience_update_form(self):
        cook = Cook.objects.create_user(
            username='chef123', password='password123', years_of_experience=5
        )
        form_data = {
            'years_of_experience': 3,
        }
        form = CookExperienceUpdateForm(data=form_data, instance=cook)
        self.assertTrue(form.is_valid())

    def test_invalid_experience_update_form(self):
        cook = Cook.objects.create_user(
            username='chef123', password='password123', years_of_experience=5
        )
        form_data = {
            'years_of_experience': -1,  # Invalid
        }
        form = CookExperienceUpdateForm(data=form_data, instance=cook)
        self.assertFalse(form.is_valid())
        self.assertIn('years_of_experience', form.errors)


class CookSearchFormTest(TestCase):
    def test_valid_search_form(self):
        form_data = {
            'username': 'chef123',
        }
        form = CookSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_search_form_empty_username(self):
        form_data = {
            'username': '',
        }
        form = CookSearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)


class DishSearchFormTest(TestCase):
    def test_valid_dish_search_form(self):
        form_data = {
            'dish_type': 'Main Course',
        }
        form = DishSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_dish_search_form_empty_dish_type(self):
        form_data = {
            'dish_type': '',
        }
        form = DishSearchForm(data=form_data)
        self.assertTrue(form.is_valid())  # This field is not required


class DishTypeSearchFormTest(TestCase):
    def test_valid_dish_type_search_form(self):
        form_data = {
            'name': 'Salad',
        }
        form = DishTypeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_dish_type_search_form_empty_name(self):
        form_data = {
            'name': '',
        }
        form = DishTypeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())  # This field is not required
