# Django-PyVows

This project is an extension of pyVows to test [Django](https://www.djangoproject.com/) projects. It enables usage of core Django testing tools in a way that is in sync with pyVows workflow mindset.

PyVows is a BDD (Behaviour Driven Development) inspired by Vows for node.js

More documentation about pyVows can be found at [the project homepage](http://pyvows.org) or for mode updated usage check the project [tests itself](https://github.com/heynemann/pyvows/tree/master/tests).

Django-PyVows is in sync with the latest Django developments and supports Django 1.8.

## Usage

There is no need to modify your project to use Django-PyVows. You only have to define where is your project settings module and start calling your project urls in your tests.

```python
from pyvows import Vows, expect

from django_pyvows.context import DjangoContext

@Vows.batch
class SimpleTestVows(DjangoContext):

    def settings_module(self):
        return 'yourproject.settings'

    def topic(self):
        return self.get('/mygreaturl/')

    def should_be_a_success(self, topic):
        expect(topic.status_code).to_equal(200)

    def should_return_the_correct_response_type(self, topic):
        expect(topic).contains("Welcome!")
```

The default `settings_module` is `settings` so you should define it accordly based on your `PYTHONPATH`.

### HTTP Client

We support `django.test.Client`, the methods `DjangoContext.get` and `DjangoContext.post` are actually simple wrappers around it so [the usage](https://docs.djangoproject.com/en/1.8/topics/testing/tools/#the-test-client) is the same.

### Assertions

The available assertions in Django-PyVows are the same as in `django.test.SimpleTestCase` they were adapted to the context of BDD and PyVows.

- `contains`: reflects the `django.test.SimpleTestCase.assertContains`. Check usage at: [https://docs.djangoproject.com/en/1.8/topics/testing/tools/#django.test.SimpleTestCase.assertContains](https://docs.djangoproject.com/en/1.8/topics/testing/tools/#django.test.SimpleTestCase.assertContains)
- `redirects_to`: reflects the `django.test.SimpleTestCase.assertRedirects`. Check usage at: [https://docs.djangoproject.com/en/1.8/topics/testing/tools/#django.test.SimpleTestCase.assertRedirects](https://docs.djangoproject.com/en/1.8/topics/testing/tools/#django.test.SimpleTestCase.assertRedirects)
- `with_form_error`: reflects the `django.test.SimpleTestCase.assertFormError`. Check usage at: [https://docs.djangoproject.com/en/1.8/topics/testing/tools/#django.test.SimpleTestCase.assertFormError](https://docs.djangoproject.com/en/1.8/topics/testing/tools/#django.test.SimpleTestCase.assertFormError)

### Settings Override

TODO