from django.urls import path
from inmuebleslist_app.api.views import ComentarioDetail, ComentarioList, EdificacionDetalleAV, EdificacionListAV, EmpresaAV, EmpresaDetalleAV

urlpatterns = [
    path('edificacion/', EdificacionListAV.as_view(), name= 'edificacion-list'),
    path('edificacion/<int:pk>', EdificacionDetalleAV.as_view(), name= 'edificacion-detail'),
    path('empresa/', EmpresaAV.as_view(), name= 'empresa'),
    path('empresa/<int:pk>', EmpresaDetalleAV.as_view(), name= 'empresa-detail'),
    path('edificacion/<int:pk>/comentario/', EdificacionDetalleAV.as_view(), name= 'comentario-list'),
    path('edificacion/comentario/<int:pk>', ComentarioDetail.as_view(), name= 'comentario-detail'),
]
