from inmuebleslist_app.api.pagination import EdificacionPagination
from inmuebleslist_app.models import Comentario, Empresa, Edificacion
from inmuebleslist_app.api.serializers import ComentarioSerializer, EmpresaSerializer, EdificacionSerializer
from rest_framework.response import Response
#from rest_framework.decorators import api_view
from rest_framework import status, generics, mixins, viewsets, filters
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from inmuebleslist_app.api.permissions import IsAdminOrReadOnly, IsComentarioUserOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from inmuebleslist_app.api.throttling import ComentarioCreateThrottle, ComentarioListThrottle
from django_filters.rest_framework import DjangoFilterBackend

class UsuarioComentario(generics.ListAPIView):
    serializer_class = ComentarioSerializer
    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Comentario.objects.filter(comentario_user__username=username)
    def get_queryset(self):
        username = self.request.query_params.get('username',None)
        return Comentario.objects.filter(comentario_user__username=username)

class ComentarioCreate(generics.CreateAPIView):
    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ComentarioCreateThrottle]
    def get_queryset(self):
        return Comentario.objects.all()
    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        inmueble = Edificacion.objects.get(pk=pk)
        user = self.request.user
        comentario_queryset = Comentario.objects.filter(edificacion=inmueble,comentario_user=user)
        if(comentario_queryset.exists()):
            raise ValidationError("El usuario ya escribio un comentario para este inmueble")
        if(inmueble.number_calificacion == 0):
            inmueble.avg_calificacion = serializer.validated_data['calificacion']
        else:
            inmueble.avg_calificacion = ((inmueble.avg_calificacion * inmueble.number_calificacion) + serializer.validated_data['calificacion']) / (inmueble.number_calificacion + 1)
        inmueble.number_calificacion = inmueble.number_calificacion + 1
        inmueble.save()
        serializer.save(edificacion=inmueble, comentario_user=user)

class ComentarioList(generics.ListCreateAPIView):
    serializer_class = ComentarioSerializer
    #permission_classes = [IsAuthenticated]
    throttle_classes = [ComentarioListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['comentario_user__username', 'active']
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Comentario.objects.filter(edificacion=pk)
            
class ComentarioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    permission_classes = [IsComentarioUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'comentario-detail'

class EmpresaVS(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    
class EdificacionList(generics.ListAPIView):
    queryset = Edificacion.objects.all()
    serializer_class = EdificacionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['direccion','empresa__nombre']
    pagination_class = EdificacionPagination

class EmpresaAV(APIView):
    def get(self, request):
        empresas = Empresa.objects.all()
        serializer = EmpresaSerializer(empresas, many=True, context={'request': request})
        return Response(serializer.data)
    def post(self, request):
        serializer = EmpresaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmpresaDetalleAV(APIView):
    def get(self, request, pk):
        try: 
            empresa = Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            return Response({'error': 'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmpresaSerializer(empresa, context={'request':request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        try: 
            empresa = Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            return Response({'error': 'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmpresaSerializer(empresa, data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
    def delete(self, request, pk):
        try: 
            empresa = Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            return Response({'error': 'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        empresa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class EdificacionListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request):
        inmuebles = Edificacion.objects.all()
        serializer = EdificacionSerializer(inmuebles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EdificacionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EdificacionDetalleAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request, pk):
        try:
            inmueble = Edificacion.objects.get(pk=pk)
            serializer = EdificacionSerializer(inmueble)
            return Response(serializer.data)
        except Edificacion.DoesNotExist:
            return Response({'Error': 'Inmueble no existe'},status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        try: 
            inmueble = Edificacion.objects.get(pk=pk)
        except Edificacion.DoesNotExist:
            return Response({'Error': 'Inmueble no existe'},status=status.HTTP_404_NOT_FOUND)
        serializer = EdificacionSerializer(inmueble, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    def delete(self, request, pk):
        try:
            inmueble = Edificacion.objects.get(pk=pk)
        except Edificacion.DoesNotExist:
            return Response({'Error': 'Inmueble no existe'},status=status.HTTP_404_NOT_FOUND)
        inmueble.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
