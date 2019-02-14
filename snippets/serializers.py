from rest_framework import serializers
from posts.models import *


class SignelsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Signels
		fields = '__all__'