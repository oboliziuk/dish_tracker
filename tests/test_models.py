from django.test import TestCase
from dishops.models import DishType, Cook, Dish


class DishTypeModelTest(TestCase):
    def setUp(self):
        self.dish_type1 = DishType.objects.create(name="Salad")
        self.dish_type2 = DishType.objects.create(name="Main Course")
        self.dish_type3 = DishType.objects.create(name="Appetizer")

    def test_string_representation(self):
        self.assertEqual(str(self.dish_type1), self.dish_type1.name)

    def test_dish_type_ordering(self):
        dish_types = list(DishType.objects.all())
        self.assertIn(self.dish_type1, dish_types)
        self.assertIn(self.dish_type2, dish_types)
        self.assertIn(self.dish_type3, dish_types)
        self.assertEqual(len(dish_types), 3)


class CookModelTest(TestCase):
    def setUp(self):
        self.cook = Cook.objects.create(
            username="chef123",
            password="password123",
            first_name="Gordon",
            last_name="Ramsay",
            years_of_experience=20
        )

    def test_string_representation(self):
        self.assertEqual(str(self.cook), "chef123 (Gordon Ramsay)")

    def test_get_absolute_url(self):
        self.assertEqual(self.cook.get_absolute_url(), "/cooks/1/")  # Замініть 1 на актуальний ID


class DishModelTest(TestCase):
    def setUp(self):
        self.dish_type = DishType.objects.create(name="Dessert")
        self.cook = Cook.objects.create(
            username="pastrychef",
            password="password123",
            first_name="Julia",
            last_name="Child"
        )
        self.dish = Dish.objects.create(
            name="Chocolate Cake",
            description="A rich chocolate cake.",
            price=12.99,
            dish_type=self.dish_type
        )
        self.dish.cooks.add(self.cook)

    def test_string_representation(self):
        self.assertEqual(str(self.dish), "Chocolate Cake")

    def test_dish_price(self):
        self.assertEqual(self.dish.price, 12.99)

    def test_related_cooks(self):
        self.assertIn(self.cook, self.dish.cooks.all())
