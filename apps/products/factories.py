import factory

from apps.users.factories import CustomUserFactory

from .models import Category, Image, Product


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"category{n}")
    parent = None
    slug = factory.Sequence(lambda n: f"slug{n}")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    user = factory.SubFactory(CustomUserFactory)
    category = factory.SubFactory(CategoryFactory)
    sku = factory.Sequence(lambda n: f"sku{n}")
    name = factory.Sequence(lambda n: f"product{n}")
    brand = factory.Sequence(lambda n: f"brand{n}")
    price = factory.Faker("pydecimal", min_value=0, left_digits=3, right_digits=1)
    wholesale_quantity = factory.Faker("pyint", min_value=2, max_value=10)
    video = factory.django.FileField(filename="example.mp4")
    quantity_in_stock = factory.Faker("pyint", min_value=1, max_value=100)
    description = factory.Faker("paragraph")
    manufacturer_country = factory.Faker("country")

    @factory.post_generation
    def create_image(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            ImageFactory(product=self)


class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Image

    product = factory.SubFactory(ProductFactory)
    image = factory.django.ImageField(filename="example.jpg")
