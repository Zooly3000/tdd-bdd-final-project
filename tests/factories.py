import factory
from service.models import Product, Category

class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("word")
    description = factory.Faker("sentence")
    price = factory.Faker("pyfloat", left_digits=2, right_digits=2, positive=True)
    available = factory.Faker("boolean")
    category = factory.Iterator(Category)  # перебирает все значения Enum
