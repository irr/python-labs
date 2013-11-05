# -*- coding: utf-8 -*-

# Python 2.6+ future compatibility declarations
# from __future__ import absolute_import, division, print_function, unicode_literals

def my_function():

    foo = 12  # NOQA
    bar = "Toholampi city coders - http://www.toholampi.fi"  # NOQA
    baz = 3.0  # NOQA

    print("Foo %(foo)s, bar %(bar)s and baz %(baz)s went to a bar..." \
        % locals())
    # versus
    # print("Foo %s, bar %s and baz %s went to a bar..." % \
    #    (foo, bar, baz))

my_function()