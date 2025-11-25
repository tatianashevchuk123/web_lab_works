from django.db import models

# Create your models here.

# -*- coding: utf-8 -*-

from django.utils import timezone

from django.db import models
from django.urls import reverse


from django.urls import reverse

class Category(models.Model):
    category = models.CharField(
        verbose_name=u'Категорія',
        max_length=250,
        help_text=u'Максимум 250 сим.'
    )
    slug = models.SlugField(u'Слаг')
    objects = models.Manager()

    class Meta:
        verbose_name = u'Категорія для публікації'
        verbose_name_plural = u'Категорії для публікацій'

    def __str__(self):
        return self.category

    def get_absolute_url(self):
        try:
            url = reverse('articles-category-list',
                          kwargs={'slug': self.slug})
        except:
            url = "/"
        return url

class Article(models.Model):
    pub_date = models.DateTimeField()
    title = models.CharField(max_length=200)
    slug = models.SlugField('Слаг', unique_for_date='pub_date')
    description = models.TextField()
    main_page = models.BooleanField(
        'Головна',
        default=True,
        help_text='Показувати на головній сторінці'
    )
    category = models.ForeignKey(
        Category,
        related_name='articles',
        blank=True,
        null=True,
        verbose_name='Категорія',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Статя'
        verbose_name_plural = 'Статті'

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date']
        verbose_name = u'Публікація'
        verbose_name_plural = u'Публікації'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        try:
            url = reverse('news-detail',
                          kwargs={
                              'year': self.pub_date.strftime("%Y"),
                              'month': self.pub_date.strftime("%m"),
                              'day': self.pub_date.strftime("%d"),
                              'slug': self.slug,
                          })
        except:
            url = "/"
        return url


class ArticleImage(models.Model):
    article = models.ForeignKey(Article,
                                verbose_name=u'Стаття',
                                related_name='images',
                                on_delete=models.CASCADE)
    image = models.ImageField(u'Фото', upload_to='photos')
    title = models.CharField(u'Заголовок', max_length=250,
                             help_text=u'Максимум 250 сим.',
                             blank=True)

    class Meta:
        verbose_name = u'Фото для статті'
        verbose_name_plural = u'Фото для статті'

    def __str__(self):
        return self.title

    @property
    def filename(self):
        return self.image.name.rsplit('/', 1)[-1]

