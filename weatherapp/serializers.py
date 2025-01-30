from rest_framework import serializers

class WeatherForecastSerializer(serializers.Serializer):
    date = serializers.IntegerField(source='dt')
    temperature=serializers.FloatField(source='main.temp')
    feels_like=serializers.FloatField(source='main.feels_like')
    humidity=serializers.IntegerField(source='main.humidity')
    weather = serializers.SerializerMethodField()
    wind_speed=serializers.FloatField(source='wind.speed')

    def get_weather(self,obj):
        return obj['weather'][0]['description'] if obj.get('weather') and len(obj['weather'])>0 else None