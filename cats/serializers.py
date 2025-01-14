import datetime as dt

from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import CHOISE, Achievement, AchievementCat, Cat, Owner


class AchievementSerializator(serializers.ModelSerializer):
    achievement_name = serializers.CharField(source='name')

    class Meta:
        model = Achievement
        fields = ('id', 'name')


class CatListSerializer(serializers.ModelSerializer):
    color = serializers.ChoiceField(choices=CHOISE)

    class Meta:
        model = Cat
        fields = ('id', 'name', 'color')


class CatSerializer(serializers.ModelSerializer):
    achievements = AchievementSerializator(many=True, required=False)
    age = serializers.SerializerMethodField()
    color = serializers.ChoiceField(choices=CHOISE)

    class Meta:
        model = Cat
        fields = (
            'id',
            'name',
            'color',
            'birth_year',
            'owner',
            'achievements',
            'age'
        )

    def create(self, validated_data):
        if 'achievements' not in self.initial_data:
            cat = Cat.objects.create(**validated_data)
            return cat

        achievements = validated_data.pop('achievements')
        cat = Cat.objects.create(**validated_data)

        for achievement in achievements:
            current_achievement, status = Achievement.objects.get_or_create(
                **achievement)
            AchievementCat.objects.create(
                achievement=current_achievement, cat=cat)
        return cat

    def get_age(self, obj):
        return dt.datetime.now().year - obj.birth_year

    @action(detail=False, url_path='recent-white-cats')
    def recent_white_cats(self, request):
        cats = Cat.objects.filter(colore='White')[:5]
        serializer = self.get_serializer(cats, many=True)
        return Response(serializer.data)


class OwnerSerializer(serializers.ModelSerializer):
    cats = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Owner
        fields = ('first_name', 'last_name', 'cats')
