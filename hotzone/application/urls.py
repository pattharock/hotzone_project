from django.urls import path
import application.views.home_views as home_views
import application.views.login_views as login_views
import application.views.registration_views as registration_views

from django.conf.urls import url
from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

app_name = 'application'

urlpatterns = [
    # authentication
    path('', login_views.loginPage.as_view(), name='login_page'),
    path('register/', registration_views.registerPage, name='register_page'),
    path('login/auth', login_views.login_auth, name='login_auth'),

    url(r'^logout/$', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),

    # home
    #path('home/', home_views.homePage.as_view(), name = 'home'),
    path('home/', home_views.create_coord, name='create_coord'),

    # confirmed case record
    path('cluster/', home_views.cluster_view, name="cluster_view"),
    path('case_list/', home_views.case_list, name='case_list'),
    path('create_patient/', home_views.create_patient, name='create_patient'),
    path('create_virus/', home_views.create_virus, name='create_virus'),
    path('get_geodata/', home_views.get_geodata, name='get_geodata'),
    path('create_coord/', home_views.create_coord, name='create_coord'),
    path('create_location/', home_views.create_location, name='create_location'),
    path('create_case/', home_views.create_case, name='create_case')

]
