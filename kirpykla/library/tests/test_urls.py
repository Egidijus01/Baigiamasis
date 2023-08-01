from django.test import TestCase
from django.urls import reverse, resolve
from library.views import barber, barber_list


class TestUrls(TestCase):
 

    def test_authors_url_is_resolved(self):
        url = reverse('barbers')
        self.assertEqual(resolve(url).func, barber_list)

    def test_barber_url_is_resolved(self):
        url = reverse('barber', args=[1])
        self.assertEqual(resolve(url).func, barber)