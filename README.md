Django pyvows
===============


Pyvows
-------

pyvows is a BDD (Behaviour Driven Development) inspired by Vows for node.js

More documentation about pyvows can be found at the project homepage

http://pyvows.org

Django-pyvows
--------------


Add to the 

    INSTALLED_APPS = (
                        ....
                        'django_pyvows',
                        ....
                     )

And create the vows as you usually would

    from pyvows import Vows, expect

    from django_pyvows.context import DjangoContext

    @Vows.batch
    class ContextTest(Vows.Context):

        def topic(self):
            return DjangoContext.start_environment(None)

        def should_be_an_error(self, topic):
            expect(topic).to_be_an_error()
