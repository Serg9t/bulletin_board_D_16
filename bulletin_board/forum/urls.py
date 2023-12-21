from django.urls import path

from . import views


urlpatterns = [
    path('', views.AnnouncementView.as_view(), name='home'),
    path('post/<int:announcement_id>/', views.DetailAnnouncementView.as_view(), name='post'),
    path('post/addpage/', views.AddAnnouncement.as_view(), name='add_page'),
    path('post/update/<int:pk>/', views.UpdateAnnouncement.as_view(), name='update_post'),
    path('post/delete/<int:pk>/', views.DeleteAnnouncement.as_view(), name='delete_post'),
    path('response/add/<int:pk>/', views.add_response, name='add_response'),
    path('response/list/<announcement_id>/', views.ListResponseFilter.as_view(), name='list_response'),
    path('response/accept/<int:pk>/', views.AcceptResponse.as_view(), name='accept_response'),
    path('response/delete/<int:pk>/', views.DeleteResponse.as_view(), name='delete_response'),
    path('news/', views.send_news_admin, name='send_news'),
    path('response<int:pk>/', views.DetailResponse.as_view(), name='response'),

]
