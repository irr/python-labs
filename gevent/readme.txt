How can I test to see whether gevent monkey patching is active?
is_monkeypatched = gevent.fork == os.fork
