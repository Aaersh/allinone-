from django.urls import path
from . import views
# from views import/ add_preprocessed_data_to_database
#URL conf
urlpatterns = [
    path('recordcount/', views.number_ofrecords),
    path('ans/', views.add_preprocessed_data_to_database),
    path('meansalary/',views.analysis_2),
    path('mediansalary/', views.analysis_3),
    path('update/', views.updating),
    path('one/', views.oneapi)
    
]
