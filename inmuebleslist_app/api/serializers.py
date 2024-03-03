from rest_framework import serializers
from inmuebleslist_app.models import Empresa, Edificacion

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'

class EdificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edificacion
        fields = '__all__'
        #exclude = ["id"]
    
    # def get_longitud_direccion(self, obj):
    #     return len(obj.direccion) 
    # def validate(self, data):
    #     if data['direccion'] == data["pais"]:
    #         raise serializers.ValidationError("El pais y la direccion deben ser distintos")
    #     return data    
    # def validate_imagen(self, data):
    #     if len(data) < 2:
    #         raise serializers.ValidationError("La imagen no puede tener menos de 2 caracteres")
    #     return data

# def column_longitude(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("El valor es demasiado corta")

# class InmuebleSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     direccion = serializers.CharField(max_length=250, validators=[column_longitude])
#     pais = serializers.CharField(max_length=150, validators=[column_longitude])
#     descripcion = serializers.CharField(max_length=500)
#     imagen = serializers.CharField(max_length=900)
#     active = serializers.BooleanField(default=True)
    
#     def create(self, validated_data):
#         return Inmueble.objects.create(**validated_data)
#     def update(self, instance, validated_data):
#         instance.direccion = validated_data.get('direccion', instance.direccion)
#         instance.pais = validated_data.get('pais', instance.pais)
#         instance.descripcion = validated_data.get('descripcion', instance.descripcion)
#         instance.imagen = validated_data.get('imagen', instance.imagen)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
#     def validate(self, data):
#         if data['direccion'] == data["pais"]:
#             raise serializers.ValidationError("El pais y la direccion deben ser distintos")
#         return data    
    
#     def validate_imagen(self, data):
#         if len(data) < 2:
#             raise serializers.ValidationError("La imagen no puede tener menos de 2 caracteres")
#         return data