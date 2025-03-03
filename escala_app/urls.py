from django.urls import path
from .views import FirebaseLoginView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("auth/login/", FirebaseLoginView.as_view(), name="firebase-login"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
]


# from django.conf.urls import url
# from escala_app import views

# app_name = 'escala_app'

# urlpatterns = [
#     #Médicos Url
#     url('medicos/register/', views.MedicosCreateView.as_view(), name='medicosregister'),
#     url(r'^medicos/$', views.MedicosListView.as_view(), name='medicoslist'),
#     url(r'^medicos/(?P<pk>[-\w]+)/$',views.MedicosDetailView.as_view(),name='detail'),
#     url(r'^medicos/update/(?P<pk>\d+)/$', views.MedicosUpdateView.as_view(), name='update'),
#     # Postos Url
#     url(r'^postos/$', views.PostosListView.as_view(), name='postoslist'),
#     url(r'^postos/register/$', views.PostosCreateView.as_view(), name='postosregister'),
#     url(r'^postos/(?P<pk>[-\w]+)/$', views.PostosDetailView.as_view(), name='postosdetail'),
#     url(r'^postos/update/(?P<pk>[-\w]+)/$', views.PostosUpdateView.as_view(), name='postosupdate'),
#     #Dia de Folga Url
#     url(r'^dia_de_folga/register/$', views.FolgaCreateView.as_view(), name='folgaregister'),
#     url(r'^dia_de_folga/$', views.FolgaListView.as_view(), name='folgalist'),
#     url(r'^dia_de_folga/delete/(?P<pk>\d+)/$',views.FolgaDeleteView.as_view(),name='delete'),
#     url(r'^dia_de_folga/update/(?P<pk>\d+)/$', views.FolgaUpdateView.as_view(), name='folgaupdate'),
#     #Escala Url
#     url(r'^escala/register/$', views.EscalaCreateView.as_view(), name='escalaregister'),
#     url(r'^escala/$', views.EscalaListView.as_view(), name='escalalist'),
#     url(r'^escala/delete/(?P<pk>\d+)/$',views.EscalaDeleteView.as_view(),name='escaladelete'),
#     url(r'^escala/update/(?P<pk>\d+)/$', views.EscalaUpdateView.as_view(), name='escalaupdate'),
# ]