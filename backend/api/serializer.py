from .models import BackendUser, Item

from rest_framework import serializers

class BackendUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = BackendUser
        fields = ['username','password']

    def create(self, validated_data):
        user = BackendUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            isadmin=False,
        )
        return user

class Itemserializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ['user']

class Itemgetserializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['id','name','price','description']

