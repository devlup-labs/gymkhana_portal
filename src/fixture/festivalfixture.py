import factory
import random

COLOUR = ["yellow", "black", "purple", "red", "orange", "green", '#084594', '#2171b5', '#4292c6', '#6baed6', '#9ecae1',
          '#c6dbef', '#deebf7', '#f7fbff'
          ]


class FestivalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'festivals.Festival'

    name = random.choice(['Ignus', 'Varchas', 'Spandan', 'Nimble'])
    tag_line = factory.Faker('sentence', nb_words=3)
    photo = factory.django.ImageField(color=random.choice(COLOUR))
    about = factory.Faker('sentence', nb_words=30)
    slug = factory.Sequence(lambda n: 'fest-%d' % n)
    link = factory.Faker('url')
    published = random.choice([True, False])
    use_custom_html = False


class EventCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'festivals.EventCategory'

    name = factory.Faker('sentence', nb_words=3)
    festival = factory.SubFactory(FestivalFactory)
    cover = factory.django.ImageField(color=random.choice(COLOUR))
    slug = factory.Sequence(lambda n: 'category-%d' % n)
    about = factory.Faker('sentence', nb_words=10)


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'festivals.Event'

    event_category = factory.SubFactory(EventCategoryFactory)
    name = factory.Faker('sentence', nb_words=3)
    slug = factory.Sequence(lambda n: 'event-%d' % n)
    unique_id = factory.Sequence(lambda n: 'event-%d' % n)
    # description = factory.Faker('sentence', nb_words=30)
    cover = factory.django.ImageField(color=random.choice(COLOUR))
    max_team_size = 1
    min_team_size = 1
    published = True
