from django.db import models
from django.contrib.auth.models import User, PermissionsMixin, AbstractBaseUser
from django.utils.crypto import get_random_string
# Create your models here


class Member(models.Model):
    MEMBER_STATE = [
        ('Not Verified', 'Not Verified'),
        ('Verified', 'Verified'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=50, choices=MEMBER_STATE)
    # jwt_token_key = models.CharField(max_length=12, default=get_random_string)

    def __str__(self):
        return self.user.get_username()


class Notification(models.Model):
    NOTIFICATION_CATEGORY = [
        ('System', 'System'),
        ('Crypto Signal', 'Crypto Signal'),
        ('Friend', 'Friend'),
    ]
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="notifications_member")
    category = models.CharField(max_length=50, choices=NOTIFICATION_CATEGORY)
    title = models.CharField(max_length=50)
    content = models.TextField()
    state = models.CharField(max_length=50)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Following(models.Model):
    FOLLOWING_STATE = [
        ('Muted', 'Muted'),
        ('All', 'All'),
        ('Partial', 'Partial'),
    ]
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    crypto_id = models.CharField(max_length=200)
    crypto_symbol = models.CharField(max_length=200)
    state = models.CharField(max_length=50, choices=FOLLOWING_STATE)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.crypto_id


class SavedFilterGroup(models.Model):
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    group_name = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    # filters = models.ManyToManyField(
    #     'filter.Filter',
    #     related_name='saved_filter_group_filter',
    # )
    # filter_details = models.OneToManyField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.group_name


class FilterDetail(models.Model):
    filter_group = models.ForeignKey(
        'SavedFilterGroup', on_delete=models.CASCADE)
    filter = models.ForeignKey('filter.Filter', on_delete=models.CASCADE)
    state = models.CharField(max_length=50)
    first_argument = models.BigIntegerField(blank=True, null=True)
    second_argument = models.BigIntegerField(blank=True, null=True)
    third_argument = models.BigIntegerField(blank=True, null=True)
    fourth_argument = models.BigIntegerField(blank=True, null=True)
    fifth_argument = models.BigIntegerField(blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.state
