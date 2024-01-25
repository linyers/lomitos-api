from rest_framework import serializers
from .models import Lomito, Rating, NightTime, DayTime
from .validations import CustomValidations

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('rate', 'reviews',)


class DayTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayTime
        fields = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',)


class NightTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NightTime
        fields = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',)


class LomitoSerializer(serializers.ModelSerializer):
    rating = RatingSerializer(many=False, required=False)
    day_time = DayTimeSerializer(many=False, required=False)
    night_time = NightTimeSerializer(many=False, required=False)

    class Meta:
        model = Lomito
        fields = ('id', 'name', 'phone', 'maps', 'logo', 'rating', 'day_time', 'night_time')

    def validate(self, data):
        CustomValidations(data)
        return data

    def create(self, validated_data):
        default_time = {
        "sunday": None,
        "monday": None,
        "tuesday": None,
        "wednesday": None,
        "thursday": None,
        "friday": None,
        "saturday": None
        }
        default_rating = {"rate": None, "reviews": None}

        rating_data = validated_data.pop('rating', default_rating)
        day_time_data = validated_data.pop('day_time', default_time)
        night_time_data = validated_data.pop('night_time', default_time)

        rating = Rating.objects.create(**rating_data)
        day_time = DayTime.objects.create(**day_time_data)
        night_time = NightTime.objects.create(**night_time_data)

        user = self.context['request'].user
        lomito, created = Lomito.objects.update_or_create(rating=rating, day_time=day_time, night_time=night_time, user=user,**validated_data)

        return lomito
    
    def update(self, instance, validated_data):
        if validated_data.get('rating'):
            rating_data = validated_data.pop('rating')
            Rating.objects.filter(pk=instance.rating.pk).update(**rating_data)
            rating = Rating.objects.get(pk=instance.rating.pk)
            instance.rating = rating

        if validated_data.get('day_time'):
            day_time_data = validated_data.pop('day_time')
            DayTime.objects.filter(pk=instance.day_time.pk).update(**day_time_data)
            day_time = DayTime.objects.get(pk=instance.day_time.pk)
            instance.day_time = day_time

        if validated_data.get('night_time'):
            night_time_data = validated_data.pop('night_time')
            NightTime.objects.filter(pk=instance.night_time.pk).update(**night_time_data)
            night_time = NightTime.objects.get(pk=instance.night_time.pk)
            instance.night_time = night_time

        instance = super().update(instance, validated_data)

        return instance