Django pyvows
===============


Pyvows
-------

pyvows is a BDD (Behaviour Driven Development) inspired by Vows for node.js

More documentation about pyvows can be found at the project homepage

http://pyvows.org

Django-pyvows
--------------


There is no need to modify your project to use Django-PyVows. You only have to create the vows
as you usually would, start the server and call your project urls:

    from pyvows import Vows, expect

    from django_pyvows.context import DjangoHTTPContext

    @Vows.batch
    class ContextTest(DjangoHTTPContext):

        def setup(self):
            self.start_server()

        def topic(self):
            return self.get('/mygreaturl/')

        def should_be_a_success(self, topic):
            expect(topic.getcode()).to_equal(200)

        def should_return_the_correct_response_type(self, topic):
            expect(topic.headers.type).to_equal("text/html")

To work you only need to override the `get_settings` method from DjangoHTTPContext to 
return the path of your settings module. The default `get_settings` returns `"settings"`.
