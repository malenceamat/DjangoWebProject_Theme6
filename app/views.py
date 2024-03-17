"""
Definition of views.
"""


from django.contrib.auth.forms import UserCreationForm # использование встроенной формы регистрации
from django.shortcuts import render, redirect # импорт функций render и redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from .forms import PoolForm # использование формы обратной связи пользователя сайта

# использование модели, которая была определена для блога в файле models.py:
from django.db import models 
from .models import Blog # использование модели данных блога
from .models import Comment # использование модели комментариев
from .forms import CommentForm # использование формы ввода комментария

from .forms import BlogForm # использование формы для ввода статьи блога

# метод действия контроллера registration для обработки данных и передачи данных с сервера для отображения шаблона веб-страницы регистрации:
def registration(request):
    """Renders the registration page."""
    assert isinstance(request, HttpRequest)
    # Для проверки наличия данных формы проверяется значение переменной method в объекте запроса request. 
    # Когда оно равняется ‘POST’ , можно получить данные формы, обращаясь к словарю POST в объекте запроса. 
    if request.method == "POST": # после отправки формы
        # Создать экземпляр класса формы, передав в функцию создания объекта формы атрибут request.POST, т.е. обращаясь к словарю POST в объекте запроса.
        # Ключами записей словаря являются в данном случае имена полей формы, заданные атрибутами name в тегах элементов формы.
        regform = UserCreationForm (request.POST)
        if regform.is_valid(): # выполняется валидация полей формы
        # Метод is_valid() выполняет проверку корректности заполнения формы (валидацию) и возвращает 
        # логическое значение, информирующее об успешной проверке. 
            reg_f = regform.save(commit=False) # не сохраняем автоматически данные формы
            # Итак: 
            #   В форме регистрации порльзователей UserCreationForm заполняются значения полей: username, password
            #   Значения некоторых полей (first_name, last_name, email) заполняются в административном разделе
            #   Значения остальных полей модели заполняются в данном методе действия контроллера:
            reg_f.is_staff = False # запрещен вход в административный раздел
            reg_f.is_active = True # активный пользователь
            reg_f.is_superuser = False # не является суперпользователем
            reg_f.date_joined = datetime.now() # дата регистрации
            reg_f.last_login = datetime.now() # дата последней авторизации

            reg_f.save() # сохраняем изменения после добавления данных
        
            return redirect('home') # переадресация на главную страницу после регистрации
    else:
        regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя

    assert isinstance(request, HttpRequest)
    return render(request,
    'app/registration.html',
    {
        'title':'Регистрация',
        'regform': regform, # передача формы в шаблон веб-страницы
        'year':datetime.now().year,
    }
)

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )


def pool(request):
    """Renders the pool page."""
    assert isinstance(request, HttpRequest)
    data = None
    # Создаются словари gender и rating, используемые в дальнейшем 
    # для получения текста выбранных пользователем полей по их значению,
    # передаваемому из формы:
    gender = {'1': 'Мужской', '2': 'Женский'}
    rating = {'1':'Отлично', '2':'Хорошо',
              '3':'Сойдет', '4':'Ужасно'}

    # код работы с формой обратной связи пользователя сайта
    # В данном случае в шаблоне страниц Django использованы обычные HTML-формы вместо собственных классов форм, представляющих модель формы. 
    # Т.е. включения форм в шаблон произведено не через переменную класса, как в других случаях.
    # Для проверки наличия данных формы проверяется значение переменной method в объекте запроса request. 
    # Когда оно равняется ‘POST’ , можно получить данные формы, обращаясь к словарю POST в объекте запроса. 
    if request.method == "POST": # после отправки данных формы на сервер методом POST
        # Создать экземпляр класса формы, передав в функцию создания объекта формы атрибут request.POST, т.е. обращаясь к словарю POST в объекте запроса.
        # Ключами записей словаря являются в данном случае имена полей формы, заданные атрибутами name в тегах элементов формы.
        form = PoolForm(request.POST)
        if form.is_valid(): # выполняется валидация полей формы
        # Метод is_valid() выполняет проверку корректности заполнения формы (валидацию) и возвращает 
        # логическое значение, информирующее об успешной проверке. 
            # Если is_valid() вернет True, проверенные данные доступны в методе действия через атрибут cleaned_data. 
            # По сути form.cleaned_data - словарь по ключам, являющийся текстовыми строками, содержащими имена полей класса формы.
            # Эти данные можно сохранить в базе данных, или выполнить с ними какие-то другие действия.
            # Создается в методе действия переменная-словарь вызовом функции dict() 
            data = dict()
            # случае успешной валидации результата, данные полей формы переносятся в словарь data
            # по ключам, являющимся текстовыми строками, содержащими имена полей класса формы
            # (в дальнейшем сохраненный в словаре по ключам набор данных будет передаваться в шаблон страницы):
            data['name'] = form.cleaned_data['name']
            data['city'] = form.cleaned_data['city']
            data['job'] = form.cleaned_data['job']
            data['gender'] = gender[ form.cleaned_data['gender'] ]
            data['design'] = rating[ form.cleaned_data['design'] ]
            data['content'] = rating[ form.cleaned_data['content'] ]
            if(form.cleaned_data['notice'] == True):
                data['notice'] = 'Да'
            else:
                data['notice'] = 'Нет'
            if(form.cleaned_data['contact'] == True):
                data['contact'] = 'Да'
            else:
                data['contact'] = 'Нет'
            data['email'] = form.cleaned_data['email']
            data['message'] = form.cleaned_data['message']
            # переменная формы form приравнивается None (пустому значению),
            # т.е. заполненная форма не будет отображаться
            form = None
         # Если валидация пройдёт неудачно, заполненная форма будет передана 
         # обратно в шаблон страницы для редактирования содержания формы пользователем
         # Если результат не True, полученная форма снова передается в шаблон, при вызове метода render. 
         # Теперь форма не пустая и HTML форма будет содержать ранее отправленные данные, которые можно 
         # повторно отредактировать и отправить снова.
    else:
        # Если же форма не была отправлена методом POST (если пришел GET запрос), то создаётся пустая 
        # новая форма для заполнения её пользователем, она будет передана методу render для последующего 
	    # рендеринга шаблона страницы с формой.
        form = PoolForm() # создание формы обратной связи пользователя сайта

        # Затем вызывается метод render, которому в последнем аргументе передаётся 
        # словарь, содержащий переменные form и data.
    """Renders the pool page."""
    return render(
        request,
        'app/pool.html',
        # словарь, который передаётся в методе действия методу render:
        {
            'title':'Обратная связь',
            'form': form,   # переменная формы может хранить пустое значение None (не отображать форму) или быть экземпляром класса формы (отображать форму)
            'data': data    # созданный словарь data включается в передаваемый render словарь как значение, записанное по определенному ключу data.
            }
    )

def blog(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    #posts = Blog.objects.order_by('-posted') 
    posts = Blog.objects.all() # запрос на выбор всех статей блога из модели
    """Renders the blog page."""
    return render(
        request,
        'app/blog.html',
        {
            'title':'Блог',
            'posts': posts, # передача списка статей в шаблон веб-страницы
            'year':datetime.now().year,
            }
    )

def blogpost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr) # запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(post=parametr) # запрос на выбор всех комментариев данной статьи блога

    # код работы с формой добавления комментария и добавления недостающих данных в модель:
    # Для проверки наличия данных формы проверяется значение переменной method в объекте запроса request. 
    # Когда оно равняется ‘POST’ , можно получить данные формы, обращаясь к словарю POST в объекте запроса. 
    if request.method == "POST": # после отправки данных формы на сервер методом POST
        # Создать экземпляр класса формы, передав в функцию создания объекта формы атрибут request.POST, т.е. обращаясь к словарю POST в объекте запроса.
        # Ключами записей словаря являются в данном случае имена полей формы, заданные атрибутами name в тегах элементов формы.
        form = CommentForm(request.POST)
        if form.is_valid(): # выполняется валидация полей формы
        # Метод is_valid() выполняет проверку корректности заполнения формы (валидацию) и возвращает 
        # логическое значение, информирующее об успешной проверке. 
            comment_f = form.save(commit=False)
            comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
            comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату
            comment_f.post = Blog.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий
            comment_f.save() # сохраняем изменения после добавления полей
            return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария
    else:
    # Если же форма не была отправлена методом POST (если пришел GET запрос), то создаётся пустая 
    # новая форма для заполнения её пользователем, она будет передана методу render для последующего 
	# рендеринга шаблона страницы с формой.
        form = CommentForm() # создание формы для ввода комментария

    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blogpost.html',
        {
            'title': 'Блог > ' + post_1.title,
            'post_1': post_1, # передача конкретной статьи в шаблон веб-страницы
            'comments': comments, # передача всех комментариев к данной статье в шаблон веб-страницы blogpost.html
            'form': form, # передача формы добавления комментария в шаблон веб-страницы
            'year':datetime.now().year,
            }
    )

def newpost(request):
    """Renders the newpost page."""
    assert isinstance(request, HttpRequest)

    # код работы с формой для ввода статьи блога
    # Для проверки наличия данных формы проверяется значение переменной method в объекте запроса request. 
    # Когда оно равняется ‘POST’ , можно получить данные формы, обращаясь к словарю POST в объекте запроса. 
    if request.method == "POST": # после отправки данных формы на сервер методом POST
        # создать экземпляр класса формы, передав в функцию создания объекта формы атрибуты request.POST и request.FILES
        # Такой вариант создания переменной формы необходим для загрузки файлов через форму
        blogform = BlogForm(request.POST, request.FILES) 
        if blogform.is_valid(): # выполняется валидация полей формы
        # Метод is_valid() выполняет проверку корректности заполнения формы (валидацию) и возвращает 
        # логическое значение, информирующее об успешной проверке. 
            blog_f = blogform.save(commit=False)
            blog_f.posted= datetime.now() # добавляем в модель блога текущую дату
            blog_f.author = request.user # добавляем (так как этого поля нет в форме) в модель блога в поле автор авторизованного пользователя
            blog_f.save() # сохраняем изменения после добавления полей

            return redirect('blog') # переадресация на страницу 'Блог' после создания статьи Блога (добавления нового поста)
    else:
    # Если же форма не была отправлена методом POST (если пришел GET запрос), то создаётся пустая 
    # новая форма для заполнения её пользователем, она будет передана методу render для последующего 
	# рендеринга шаблона страницы с формой.
        blogform = BlogForm() # создание формы для ввода статьи блога

    """Renders the newpost page."""
    return render(
        request,
        'app/newpost.html',
        {
            'title': 'Добавить статью блога',
            'blogform': blogform, # передача формы для ввода статьи блога в шаблон веб-страницы
            'year':datetime.now().year,
            }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница с нашими контактами',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведения о нас',
            'year':datetime.now().year,
        }
    )


def links(request):
    """Renders the links page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Ресурсы',
            'message':'Ссылки на полезные ресурсы',
            'year':datetime.now().year,
        }
    )


def videopost(request):
    """Renders the video page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Видео',
            'year':datetime.now().year,
        }
    )