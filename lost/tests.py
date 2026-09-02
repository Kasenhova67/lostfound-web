from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import itemlost, itemfound
from datetime import date, time
from rest_framework.test import APIClient


class ModelsTest(TestCase):
    """Тесты моделей"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )

    def test_create_itemlost(self):
        item = itemlost.objects.create(
            product_title='Test Lost Item',
            place='Test Place',
            date=date.today(),
            time=time(12, 0),
            description='Test Description',
            contactme='test@example.com',
            username='testuser'
        )
        self.assertEqual(item.product_title, 'Test Lost Item')
        self.assertEqual(str(item), 'testuser lost Test Lost Item')

    def test_create_itemfound(self):
        item = itemfound.objects.create(
            product_title='Test Found Item',
            place='Test Place',
            date=date.today(),
            time=time(12, 0),
            description='Test Description',
            contactme='test@example.com',
            username='testuser'
        )
        self.assertEqual(item.product_title, 'Test Found Item')
        self.assertEqual(str(item), 'testuser found Test Found Item')


class ViewsTest(TestCase):
    """Тесты представлений"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_lost_list_view(self):
        """Страница списка потерь доступна"""
        response = self.client.get(reverse('lost_list'))
        self.assertEqual(response.status_code, 200)

    def test_found_list_view(self):
        """Страница списка находок доступна"""
        response = self.client.get(reverse('found_list'))
        self.assertEqual(response.status_code, 200)

    def test_lost_list_pagination(self):
        """Пагинация работает (6 элементов на страницу)"""
        for i in range(10):
            itemlost.objects.create(
                product_title=f'Item {i}',
                place='Place',
                date=date.today(),
                time=time(12, 0),
                description='Desc',
                contactme='test@example.com',
                username='testuser'
            )
        response = self.client.get(reverse('lost_list'))
        self.assertEqual(len(response.context['object']), 6)

    def test_profile_access_requires_login(self):
        """Профиль доступен только авторизованным"""
        self.client.logout()
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 302) 

    def test_create_lost_item_requires_login(self):
        """Создание объявления требует авторизации"""
        self.client.logout()
        response = self.client.get('/reportLost/')
        self.assertEqual(response.status_code, 302) 

    def test_create_lost_item_post(self):
        """Создание объявления о потере через POST"""
        data = {
            'product_title': 'New Lost Item',
            'place': 'Test Place',
            'date': date.today().isoformat(),
            'time': '12:00',
            'description': 'Test Description',
            'contactme': 'test@example.com',
            'username': 'testuser'
        }
        response = self.client.post('/reportLost/', data)
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(itemlost.objects.count(), 1)
        self.assertEqual(itemlost.objects.first().product_title, 'New Lost Item')

    def test_delete_item(self):
        """Удаление объявления работает"""
        item = itemlost.objects.create(
            product_title='To Delete',
            place='Place',
            date=date.today(),
            time=time(12, 0),
            description='Desc',
            contactme='test@example.com',
            username='testuser'
        )
        response = self.client.post(f'/profile/my_lost_things/active/{item.id}/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(itemlost.objects.count(), 0)


class SearchTest(TestCase):
    """Тесты поиска"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.item = itemlost.objects.create(
            product_title='Laptop',
            place='Library',
            date=date.today(),
            time=time(12, 0),
            description='Dell XPS 13',
            contactme='laptop@email.com',
            username='testuser'
        )

    def test_search_by_title(self):
        results = itemlost.objects.filter(product_title__icontains='Laptop')
        self.assertEqual(results.count(), 1)

    def test_search_by_place(self):
        results = itemlost.objects.filter(place__icontains='Library')
        self.assertEqual(results.count(), 1)

    def test_search_by_description(self):
        results = itemlost.objects.filter(description__icontains='XPS')
        self.assertEqual(results.count(), 1)

    def test_search_no_results(self):
        results = itemlost.objects.filter(product_title__icontains='Nonexistent')
        self.assertEqual(results.count(), 0)


class AdminTest(TestCase):
    """Тесты административной панели"""
    
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@example.com'
        )
        self.client.login(username='admin', password='admin123')

    def test_admin_access(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

    def test_admin_models_registered(self):
        from django.contrib.admin import site
        from lost.models import itemlost, itemfound
        self.assertIn(itemlost, site._registry)
        self.assertIn(itemfound, site._registry)


class APITest(TestCase):
    """Тесты REST API"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.item = itemlost.objects.create(
            product_title='API Test Item',
            place='Test Place',
            date=date.today(),
            time=time(12, 0),
            description='Test Description',
            contactme='test@example.com',
            username='testuser'
        )

    def test_api_lost_detail(self):
        """GET /api/lost/{id}/ возвращает детали"""
        response = self.client.get(f'/api/lost/{self.item.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['product_title'], 'API Test Item')

    def test_api_lost_create(self):
        """POST /api/lost/ создает объявление"""
        data = {
            'product_title': 'API Created Item',
            'place': 'API Place',
            'date': date.today().isoformat(),
            'time': '12:00',
            'description': 'API Description',
            'contactme': 'api@example.com'
        }
        response = self.client.post('/api/lost/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(itemlost.objects.count(), 2)

    def test_api_lost_delete(self):
        """DELETE /api/lost/{id}/ удаляет объявление"""
        response = self.client.delete(f'/api/lost/{self.item.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(itemlost.objects.count(), 0)

   