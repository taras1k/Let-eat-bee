from django.conf import settings
from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url(r'^$',views.homepage, name= 'home'),
    url(r'^login/$',views.login, name= 'login_page'),
    url(r'^login_social/$',views.social_login, name= 'social_login'),
    url(r'^register/$',views.register, name= 'register_page'),
    url('^setup/$', 'socialregistration.views.setup',
        name='socialregistration_setup'),

    url('^logout/$', 'socialregistration.views.logout',
        name='social_logout'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

# Setup Facebook URLs if there's an API key specified
if getattr(settings, 'FACEBOOK_API_KEY', None) is not None:
    urlpatterns = urlpatterns + patterns('',
        url('^facebook/login/$', 'socialregistration.views.facebook_login',
            name='facebook_login'),

        url('^facebook/connect/$', 'socialregistration.views.facebook_connect',
            name='facebook_connect'),

        url('^xd_receiver.htm', 'django.views.generic.simple.direct_to_template',
            {'template':'socialregistration/xd_receiver.html'},
            name='facebook_xd_receiver'),
    )

#Setup Twitter URLs if there's an API key specified
if getattr(settings, 'TWITTER_CONSUMER_KEY', None) is not None:
    urlpatterns = urlpatterns + patterns('',
        url('^twitter/redirect/$', 'socialregistration.views.oauth_redirect',
            dict(
                consumer_key=settings.TWITTER_CONSUMER_KEY,
                secret_key=settings.TWITTER_CONSUMER_SECRET_KEY,
                request_token_url=settings.TWITTER_REQUEST_TOKEN_URL,
                access_token_url=settings.TWITTER_ACCESS_TOKEN_URL,
                authorization_url=settings.TWITTER_AUTHORIZATION_URL,
                callback_url='twitter_callback'
            ),
            name='twitter_redirect'),

        url('^twitter/callback/$', 'socialregistration.views.oauth_callback',
            dict(
                consumer_key=settings.TWITTER_CONSUMER_KEY,
                secret_key=settings.TWITTER_CONSUMER_SECRET_KEY,
                request_token_url=settings.TWITTER_REQUEST_TOKEN_URL,
                access_token_url=settings.TWITTER_ACCESS_TOKEN_URL,
                authorization_url=settings.TWITTER_AUTHORIZATION_URL,
                callback_url='twitter'
            ),
            name='twitter_callback'
        ),
        url('^twitter/$', 'socialregistration.views.twitter', name='twitter'),
    )

urlpatterns = urlpatterns + patterns('',
    url('^openid/redirect/$', 'socialregistration.views.openid_redirect', name='openid_redirect'),
    url('^openid/callback/$', 'socialregistration.views.openid_callback', name='openid_callback')
)