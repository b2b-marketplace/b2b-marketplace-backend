import factory
from django.core.files.base import ContentFile

from apps.products.models import Category, Image, Product, Video
from apps.users.factories import CustomUserFactory


class CategoryFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания категорий."""

    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"category{n}")
    parent = None
    slug = factory.Sequence(lambda n: f"slug{n}")


class ProductFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания товаров."""

    class Meta:
        model = Product

    user = factory.SubFactory(CustomUserFactory)
    category = factory.SubFactory(CategoryFactory)
    sku = factory.Sequence(lambda n: f"sku{n}")
    name = factory.Sequence(lambda n: f"product{n}")
    brand = factory.Faker("word")
    price = factory.Faker("pydecimal", min_value=0, left_digits=3, right_digits=1)
    wholesale_quantity = factory.Faker("pyint", min_value=2, max_value=10)
    quantity_in_stock = factory.Faker("pyint", min_value=1, max_value=100)
    description = factory.Faker("paragraph")
    manufacturer_country = factory.Faker("country")

    @factory.post_generation
    def create_image(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            ImageFactory(product=self)

    @factory.post_generation
    def create_video(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            VideoFactory(product=self)


class ImageFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания изображений."""

    class Meta:
        model = Image

    product = factory.SubFactory(ProductFactory)
    image = factory.django.ImageField(filename="example.jpg")


class VideoFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания видео."""

    class Meta:
        model = Video

    product = factory.SubFactory(ProductFactory)

    @factory.lazy_attribute
    def video(self):
        video_path = "apps/products/factories/video_example/SampleVideo_360x240_200kb.mp4"
        with open(video_path, "rb") as file:
            video_bytes = file.read()

        video_file = ContentFile(video_bytes, "video_example.mp4")
        return video_file
