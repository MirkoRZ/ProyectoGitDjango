"""
URL configuration for printstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from productos import views
from ordenes import views as orderViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home,name='home'),
    path('productos/',views.Productos),
    path('signup/',views.signup),
    path('logout/',views.signout,name='logout'),
    path('signin/',views.signin),
    path('productos/create/',views.create_producto,name="create_producto"),
    path('productos/create/<int:producto_id>',views.create_especificacion,name="create_especificacion"),
    path('productos/create/<int:producto_id>/especificacion/<int:especificacion_id>',views.create_opcion,name="create_opcion"),
    path('productos/create/<int:producto_id>/especificacion-numerica/<int:especificacion_id>',views.create_opcion_numerica,name="create_opcion_numerica"),
    path('ordenes/',orderViews.Ordenes),
    path('ordenes/create',orderViews.Create_orden,name="Create_orden"),
    path('ordenes/send/<int:id_orden>',orderViews.entregar_orden,name="Send_orden")
]
