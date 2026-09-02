from rest_framework import serializers
from lost.models import itemlost, itemfound
from users.models import Profile

class ItemLostSerializer(serializers.ModelSerializer):
    class Meta:
        model = itemlost
        fields = ['id', 'product_title', 'place', 'date', 'time', 'description', 'contactme', 'username']
        read_only_fields = ['username']

class ItemFoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = itemfound
        fields = ['id', 'product_title', 'place', 'date', 'time', 'description', 'contactme', 'username']
        read_only_fields = ['username']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'image']
