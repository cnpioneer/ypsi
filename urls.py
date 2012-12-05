from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from psi.views import user_login
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^accounts/login/',user_login),
    #url(r'^accounts/logout/',user_logout),
    #url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^$', 'psi.views.ypsi_index'),
    url(r'^sales/$', 'psi.views.ypsi_sales'),
    url(r'^sales/add/$', 'psi.views.ypsi_sales_add'),
    url(r'^sales/search/$', 'psi.views.ypsi_sales_search'),
    url(r'^sales/show/$', 'psi.views.ypsi_sales_show'),
    url(r'^sales/mini/$', 'psi.views.ypsi_sales_mini'),
    url(r'^sales/chart/$', 'psi.views.ypsi_sales_chart'),
    url(r'^staff/$', 'psi.views.ypsi_staff'),
    url(r'^staff/list/$', 'psi.views.ypsi_staff_list'),
    url(r'^depots/$', 'psi.views.ypsi_depots'),
    url(r'^depots/charts/$', 'psi.views.ypsi_depots_charts'),
    url(r'^depots/product/$', 'psi.views.ypsi_depots_product'),
    url(r'^depots/in/$', 'psi.views.ypsi_depots_in'),
    #url(r'^depots/out/$', 'psi.views.ypsi_depots_out'),
    url(r'^depots/(out|re)/$', "psi.views.ypsi_depots_out"),
    url(r'^depots/remit/$', 'psi.views.ypsi_depots_remit'),
    url(r'^product/mini/$', 'psi.views.ypsi_product_mini'),
    url(r'^product/check/$', 'psi.views.ypsi_product_checkdata'),
    url(r'^customer/$', 'psi.views.ypsi_customer'),
    url(r'^customer/mini/$', 'psi.views.ypsi_customer_mini'),
    url(r'^customer/check/$', 'psi.views.ypsi_customer_checkdata'),
    url(r'^category/$', 'psi.views.ypsi_category'),
    url(r'^pac/$', 'psi.views.product_autocomplete'),
    url(r'^dac/$', 'psi.views.depot_autocomplete'),
    #url(r'^dpv/$', 'psi.views.depot_pView'),
    url(r'^csearch/$', 'psi.views.customer_search'),
    # url(r'^ypsi/', include('ypsi.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^i18n/', include('django.conf.urls.i18n')),
)
urlpatterns += staticfiles_urlpatterns()