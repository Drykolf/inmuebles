from rest_framework import serializers
from inmuebleslist_app.models import Comentario, Empresa, Edificacion

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        exclude = ['edificacion']
        #fields = '__all__'

class EdificacionSerializer(serializers.ModelSerializer):
    comentarios = ComentarioSerializer(many=True, read_only=True)
    class Meta:
        model = Edificacion
        fields = '__all__'
        #exclude = ["id"]
        
class EmpresaSerializer(serializers.HyperlinkedModelSerializer):
    edificacionList = EdificacionSerializer(many=True, read_only=True)
    #edificacionList = serializers.StringRelatedField(many=True, read_only=True)
    #edificacionList = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # edificacionList = serializers.HyperlinkedRelatedField(
    #     many=True, 
    #     read_only=True,
    #     view_name="edificacion-detalle"
    #     )
    class Meta:
        model = Empresa
        fields = '__all__'
