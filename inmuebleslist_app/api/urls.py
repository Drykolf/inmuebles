from django.urls import path
from inmuebleslist_app.api.views import EdificacionDetalleAV, EdificacionListAV, EmpresaAV

urlpatterns = [
    path('list/', EdificacionListAV.as_view(), name= 'edificacion-list'),
    path('<int:pk>', EdificacionDetalleAV.as_view(), name= 'edificacion-detalle'),
    path('empresa/', EmpresaAV.as_view(), name= 'empresa'),
]
