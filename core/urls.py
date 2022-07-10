from django.urls import path
from . import views

urlpatterns=[
    path('', views.MainListView.as_view(), name='main'),
    path('<slug:url>/', views.confrence,name='conference_detail'),  
    path('register/<int:pk>', views.RegisterView.as_view(), name='register_view'),
    path('work/<int:pk>', views.WorkView.as_view(), name='work_view'),
]
#     path('<slug:slug>/', views.ConferenceDetail.as_view(), name='conference_detail'),