from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'', 'Blog.urls', name='blog'),
    host(r'api', 'Api.urls', name='api'),
)
