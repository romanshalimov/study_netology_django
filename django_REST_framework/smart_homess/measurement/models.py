from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=60, default=None)
    description = models.TextField()

    def __str__(self):
        return self.name

class Measurement(models.Model):
    temperature = models.FloatField(max_length=60.00, null=False)
    data_create = models.DateTimeField(auto_now_add=True)
    data_update = models.DateTimeField(auto_now=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    image = models.ImageField(max_length=60, null=True)

    def __str__(self):
        return f'{self.temperature}, {self.data_create}, {self.data_update}, {self.sensor}'