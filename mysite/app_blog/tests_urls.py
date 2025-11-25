from django.test import TestCase
from django.urls import reverse, resolve

from .views import HomePageView, ArticleList, ArticleCategoryList, ArticleDetail
from .models import Category, Article
from datetime import date


class UrlTests(TestCase):

    def test_home_url(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve('/').func.view_class, HomePageView)

    def test_articles_list_url(self):
        url = reverse('articles-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve('/articles').func.view_class, ArticleList)

    def test_articles_category_url(self):
        Category.objects.create(category="Test Cat", slug="test-cat")
        url = reverse('articles-category-list', args=['test-cat'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve('/articles/category/test-cat').func.view_class, ArticleCategoryList)

    def test_article_detail_url(self):
        category = Category.objects.create(category="Test Cat", slug="test-cat")

        Article.objects.create(
            title="Article title",
            slug="test-article",
            pub_date=date(2023, 5, 12),
            description="text",
            category=category
        )

        url = reverse('news-detail', args=[2023, 5, 12, 'test-article'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
