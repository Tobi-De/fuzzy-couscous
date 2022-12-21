This page give more details on the structure, layouts and packages use for the project template and therefore available
in you generated project.

## DjangoFastDev

Occasionally you may see a `FastDevVariableDoesNotExist` error, this exception is thrown during template rendering
by [django-fastdev](https://github.com/boxed/django-fastdev) when you try to access a variable that is not defined in the context
context of the view associated with that template. This is intended to help you avoid typos and small errors that will
have you scratching your head for hours. But since this can be annoying for some people, you can disable it by removing `django-fastdev`
entirely or by commenting out the *django-fastdev* application in the `settings.py` file.

```python
THIRD_PARTY_APPS = [
    ...
    # 'django_fastdev',
]
```
