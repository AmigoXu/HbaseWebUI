from django.conf.urls import url
urlpatterns = [
    # ex: /polls/
    url(r'^hbase/$', views.index, name='hbase'),
    url(r'^hbase/ajax_getData/$', views.ajax_getData), 
    # ex: /polls/5/
#     url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
#     url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
#     url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
               ]