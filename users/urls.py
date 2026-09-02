from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from pages.views import home_view, about_view
from lost.views import lost_view, lost_enter, found_enter, found_view
from users.views import register, profile, updateProfile, lost, found
from users.views import post_delete_view, post_delete_view1
from users.views import specific_post_view, specific_post_view1, activelost, activefound
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('reportLost/', lost_enter, name='enter_lost'),
    path('lostlist/', lost_view, name='lost_list'),
    path('foundList/', found_view, name='found_list'),
    path('reportFound/', found_enter, name='enter_found'),
    path('about/', about_view, name='about_us'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/update/', updateProfile, name='update_info'),
    path('profile/my_lost_things/', lost, name='lost_specific'),
    path('profile/my_found_things/', found, name='found_specific'),
    path('profile/my_lost_things/active/', activelost, name='lost_specific_active'),
    path('profile/my_found_things/active/', activefound, name='found_specific_active'),
    path('profile/my_lost_things/active/<int:id>/', specific_post_view1, name='specific-post-view-l'),
    path('profile/my_found_things/active/<int:id>/', specific_post_view, name='specific-post-view-f'),
    path('profile/my_lost_things/active/<int:id>/delete/', post_delete_view1, name='product-delete-l'),
    path('profile/my_found_things/active/<int:id>/delete/', post_delete_view, name='product-delete-f'),
    path('api/', include('lost.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)