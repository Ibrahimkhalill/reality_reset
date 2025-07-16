from rest_framework import serializers
from .models import TermsAndConditions

class TermsAndConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsAndConditions
        fields = ['id', 'content', 'updated_at', 'created_at']



from .models import DailyFeeling

class DailyFeelingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyFeeling
        fields = ['id', 'user', 'intensity', 'date', 'created_at']


from .models import DailyMood

class DailyMoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyMood
        fields = ['id', 'user', 'mood', 'date', 'created_at']