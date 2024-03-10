from rest_framework import serializers
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only = True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2'] 
        extra_kwargs = {
            'password' : {'write_only': True}
        }
    def save(self):
        password = self.validated_data['password']
        if password != self.validated_data.pop('password2'):
            raise serializers.ValidationError({'error':"Las contraseñas no coinciden"})
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error':"Ya existe un usuario con este correo"})
        account = User(email=self.validated_data['email'], username = self.validated_data['username'])
        account.set_password(password)
        account.save()
        return account