from rest_framework import serializers

from filter.models import Filter


class FilterService(serializers.Serializer):

    category = serializers.CharField()
    filter_content = serializers.CharField()
    formula_id = serializers.CharField()

    def create(self, validated_data: dict) -> Filter:
        return Filter.objects.create(**validated_data)

    def update(self, instance: Filter, validated_data: dict) -> Filter:
        instance.category = validated_data['category']
        instance.filter_content = validated_data['filter_content']
        instance.formula_id = validated_data['formula_id']
        instance.save()
        return instance

    def delete(id) -> bool:
        try:
            instance = Filter.objects.get(pk=id)
            instance.delete()
            return True
        except Exception as e:
            return False

    @classmethod
    def for_instance(cls, instance_id: int, data={}) -> 'FilterService':
        filter_instance = Filter.objects.get(pk=instance_id)
        return cls(filter_instance, data=data)
