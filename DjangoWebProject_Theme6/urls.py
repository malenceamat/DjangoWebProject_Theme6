"""
Definition of urls for DjangoWebProject_Theme6.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
# Импорт соответствующих модулей библиотеки для доступа к административному разделу:
from django.conf.urls import include
from django.contrib import admin
# Инициализация административного раздела веб-сайта:
admin.autodiscover()

# Импорт функций для настройки доступа к загруженным файлам
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about$', app.views.about, name='about'),
    url(r'^pool$', app.views.pool, name='pool'), # Строка шаблона URL для страницы Обратная связь
    url(r'^videopost$', app.views.videopost, name='videopost'), # Строка шаблона URL для страницы Видео
    url(r'^links$', app.views.links, name='links'), # шаблон URL для веб-страницы, которая содержит гиперссылки с логотипами интернет-ресурсов
    url(r'^blog$', app.views.blog, name='blog'), # шаблон URL для веб-страницы со списком постов
    url(r'^(?P<parametr>\d+)/$', app.views.blogpost, name='blogpost'), # строка для перехода на страницу поста по параметру
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Авторизация',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)), # Строка шаблона URL для входа в административный раздел
    url(r'^newpost$', app.views.newpost, name='newpost'), # Строка шаблона URL для страницы добавления статьи блога (добавления нового поста)
    url(r'^registration$', app.views.registration, name='registration') # URL для веб-страницы registration

]

# Строки шаблонов URL для загрузки файлов в папку media, вложенной в папку проекта
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()