from inmuebleslist_app.models import Comentario, Empresa, Edificacion
from inmuebleslist_app.api.serializers import ComentarioSerializer, EmpresaSerializer, EdificacionSerializer
from rest_framework.response import Response
#from rest_framework.decorators import api_view
from rest_framework import status, generics, mixins, viewsets
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

class ComentarioCreate(generics.CreateAPIView):
    serializer_class = ComentarioSerializer
    def get_queryset(self):
        return Comentario.objects.all()
    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        inmueble = Edificacion.objects.get(pk=pk)
        user = self.request.user
        comentario_queryset = Comentario.objects.filter(edificacion=inmueble,comentario_user=user)
        if(comentario_queryset.exists()):
            raise ValidationError("El usuario ya escribio un comentario para este inmueble")
        serializer.save(edificacion=inmueble, comentario_user=user)

class ComentarioList(generics.ListCreateAPIView):
    #queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Comentario.objects.filter(edificacion=pk)
            
class ComentarioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

'''class ComentarioList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class ComentarioDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    '''
class EmpresaVS(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    
    '''  
class EmpresaVS(viewsets.ViewSet):
    def list(self, request):
        queryset = Empresa.objects.all()
        serializer = EmpresaSerializer(queryset, many=True)
        return Response(serializer.data)
    def retrieve(self, request, pk= None):
        queryset = Empresa.objects.all()
        edificacionList = get_object_or_404(queryset, pk=pk)
        serializer = EmpresaSerializer(edificacionList)
        return Response(serializer.data)
    def create(self,request):
        serializer = EmpresaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def update(self, request, pk):
        try:
            empresa = Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            return Response({'error': 'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmpresaSerializer(empresa, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, pk):
        try:
            empresa = Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            return Response({'error': 'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        empresa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    '''
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
    
