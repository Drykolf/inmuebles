from django.urls import path
from inmuebleslist_app.api.views import ComentarioDetail, ComentarioList, EdificacionDetalleAV, EdificacionListAV, EmpresaAV, EmpresaDetalleAV

urlpatterns = [
    path('list/', EdificacionListAV.as_view(), name= 'edificacion-list'),
    path('<int:pk>', EdificacionDetalleAV.as_view(), name= 'edificacion-detail'),
    path('empresa/', EmpresaAV.as_view(), name= 'empresa'),
    path('empresa/<int:pk>', EmpresaDetalleAV.as_view(), name= 'empresa-detail'),
    path('comentario/', ComentarioList.as_view(), name= 'comentario-list'),
    path('comentario/<int:pk>', ComentarioDetail.as_view(), name= 'comentario-detail'),
]
