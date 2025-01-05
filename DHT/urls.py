from django.urls import path
from . import views
from . import api
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login_view, name='home'),
    path('logout', views.logout_user, name='logout'),
    path("api",api.Dlist, name='json'),
    path("api/post",api.Dlist, name='json'),
    path('download_csv', views.download_csv, name='download_csv'),
    path('table',views.table, name='table'),
    path('chartTEMP', views.chartTEMP,name='myChartTemp'),
    path('chartHUM', views.chartHUM, name='myChartHum'),
    path('chart_temp_jour', views.chart_temp_jour, name='chart_temp_jour'),
    path('chart_temp_semaine', views.chart_temp_semaine, name='chart_temp_semaine'),
    path('chart_temp_mois', views.chart_temp_mois, name='chart_temp_mois'),
    path('chart_hum_jour', views.chart_hum_jour, name='chart_hum_jour'),
    path('chart_hum_semaine', views.chart_hum_semaine, name='chart_hum_semaine'),
    path('chart_hum_mois', views.chart_hum_mois, name='chart_hum_mois'),
    path('chart_data', views.chart_data, name='chart_data'),
    path('download_csv', views.download_csv, name='csv'),
    path('csv_semaine', views.csv_semaine, name='csvS'),
    path('csv_mois', views.csv_mois, name='csvM'),
    path('csv_jour', views.csv_jour, name='csvJ'),
    path('alert', views.some_view, name='alert'),
    path('archive', views.archive_view, name='archive'),


]