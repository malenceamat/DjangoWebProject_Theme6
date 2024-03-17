"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

# Комментарии для постов в блоге (импорта класса модели Comment)
from django.db import models
from .models import Comment
# Импорт модели блога
from.models import Blog

# Для авторизации пользователя на сайте Django предоставляет форму класса BootstrapAuthenticationForm. 
# Форма содержит два поля:
#     username — для ввода логина пользователя;
#     password — для ввода пароля пользователя.
# Для использования формы BootstrapAuthenticationForm в веб-проекте необходимо, 
# чтобы код класса формы был добавлен в файл проекта forms.py:

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))


# Код для формы обратной связи пользователя сайта, содержащей следующие поля:
class PoolForm (forms.Form):
    # однострочные текстовые поля ввода
    name = forms.CharField(label='Имя', min_length=2, max_length=100)       # имя
    city = forms.CharField(label='Город', min_length=2, max_length=100)      # город
    job = forms.CharField(label='Род занятий', min_length=2, max_length=100) # специальность
    # Поле gender задаёт две радиокнопки
    gender = forms.ChoiceField(label='Пол',
                             choices=[('1', 'Мужской'),('2', 'Женский')],        # Аргумент choices содержит список кортежей, задающих пары “значение”-“надпись” для радиокнопок одной группы. 
                             widget=forms.RadioSelect,                           # Аргумент widget задает виджет forms.RadioSelect, который обеспечивает отображение этого поля как набора радиокнопок
                             initial = 1                                         # Аргумент initial=1 задает выбранную по умолчанию кнопку, в данном случае - первую кнопку группы.
                             )                                                   # пол
    # Поле design задаёт раскрывающийся список 
    design = forms.ChoiceField(label='Оцените дизайн сайта', 
                             choices=(('1', 'Отлично'),                          # аргумент choices задает кортеж кортежей, содержащий пары “значение”-“надпись” для отдельных строк списка. 
                                      ('2', 'Хорошо'),
                                      ('3', 'Сойдет'),
                                      ('4', 'Ужасно'),),
                                      initial = 1                                # Аргумент initial=1 задает выбор по умолчанию для первой строки списка.
                                     )                                           # вопрос об оценке дизайна сайта
    # Поле content задаёт раскрывающийся список 
    content = forms.ChoiceField(label='Оцените актуальность контента', 
                             choices=(('1', 'Отлично'),                          # аргумент choices задает кортеж кортежей, содержащий пары “значение”-“надпись” для отдельных строк списка. 
                                      ('2', 'Хорошо'),
                                      ('3', 'Сойдет'),
                                      ('4', 'Ужасно'),),
                                      initial = 1                                # Аргумент initial=1 задает выбор по умолчанию для первой строки списка.
                                     )                                           # вопрос об оценке актуальности контента
    # Поле notice задаёт флажок. В метод действия для этого поля передаётся логическое значение True или False в зависимости от того, выбран флажок или сброшен. 
    notice = forms.BooleanField(label='Получать новости сайта на e-mail', 
                                required=False                                   # Аргумент required=False необходим, когда у пользователя должна быть возможность не выбирать флажок. 
                               )                                                 # согласие на отправку новостей сайта.

    # Поле contact задаёт флажок. В метод действия для этого поля передаётся логическое значение True или False в зависимости от того, выбран флажок или сброшен. 
    contact = forms.BooleanField(label='Разрешаю связаться со мной по поводу отзыва', 
                                required=False                                   # Аргумент required=False необходим, когда у пользователя должна быть возможность не выбирать флажок. 
                               )                                                 # согласие на отправку новостей сайта.

    # Поле email создается как экземпляр класса forms.EmailField. Это тип обеспечивает валидацию поля ввода текста в соответствии со стандартным форматом e-mail. 
    email= forms.EmailField(label='Адрес e-mail', min_length=7)                    # e-mail
    # Многострочное текстовое поле ввода задается как однострочное, но в качестве значения атрибута widget указан экземпляр класса forms.Textarea
    message = forms.CharField(label='Отзыв', 
                              widget=forms.Textarea(attrs={'rows':12,'coils':20})# При создании экземпляра forms.Textarea передается аргумент attrs, содержащий словарь параметров, задающих число текстовых строк и столбцов.
                             )                                                   # короткое резюме

# Код для формы ввода комментария на странице поста блога:
class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment # используемая модель
        fields = ('text',) # требуется заполнить только поле text
        labels = {'text': "Комментарий"} # метка к полю text формы

# Код для формы ввода статьи блога:
class BlogForm (forms.ModelForm):
    class Meta:
        model = Blog # Используемая модель
        fields = {'title', 'description', 'content', 'image',} # заполняемые поля для ввода заголовка, краткого содержания, полного содержания статьи, выбора файла картинки
        labels = {'title': "Заголовок", 'description': "Краткое содержание", 'content': "Полное содержание", 'image': "Картинка"}  # метки к полям формы
