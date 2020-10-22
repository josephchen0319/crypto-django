from django.db import models


class Filter(models.Model):

    class Meta:
        pass

    FILTER_CATEGORY = [
        ('Standard', 'Standard'),
        ('Liquidity', 'Liquidity'),
        ('Marketcap', 'Market Cap'),
        ('Volume', 'Volume'),
        ('Supply', 'Supply'),
        ('ROI', 'ROI'),
    ]
    category = models.CharField(max_length=50, choices=FILTER_CATEGORY)
    filter_name = models.CharField(max_length=50)
    filter_content = models.CharField(max_length=200)
    filter_to_api_field = models.CharField(max_length=500, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.filter_content
