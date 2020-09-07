from rest_framework import serializers

from member.models import Member
from django.contrib.auth.models import User


class MemberService(serializers.Serializer):

    state = serializers.CharField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data: dict) -> Member:
        state = validated_date['state']
        user = User.objects.create(**validated_data['user'])
        return Member.objects.create(user=user, state=state)

    def update(self, instance: Member, validated_data: dict) -> Filter:
        original_password = validated_date['original_password']
        new_password = validated_data['new_password']
        confirm_password = validated_data['confirm_password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        if instance.user.check_password(original_password) and new_password == confirm_password:
            instance.user.set_password(new_password)

        if validated_data['first_name']:
            instance.user.first_name = first_name

        if validated_data['last_name']:
            instance.user.last_name = last_name

        state = "Verified"
        instance.state = state
        instance.save()
        return instance

    def delete(id) -> bool:
        try:
            instance = Member.objects.get(pk=id)
            instance.delete()
            return True
        except Exception as e:
            return False

    @classmethod
    def for_instance(cls, instance_id: int, data={}) -> 'FilterService':
        filter_instance = Filter.objects.get(pk=instance_id)
        return cls(filter_instance, data=data)
