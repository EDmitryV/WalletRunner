from django.db import models

from pyexpat import model
from statistics import mode
from django.db import models


class Areas(models.Model):
    Area_id = models.AutoField(primary_key= True)
    Center_coords = models.TextField()
    Radius = models.FloatField()
    Creation_date = models.DateField()
    Is_Active = models.BooleanField()



class Networks(models.Model):
    Network_id = models.AutoField(primary_key=True)
    Network_name = models.TextField()




class Stores(models.Model):
    Store_id = models.AutoField(primary_key= True)
    Center_coords = models.TextField()
    Network_id = models.ForeignKey(Networks, on_delete=models.DO_NOTHING)


class Area_Store(models.Model):
    Area_id = models.ForeignKey(Areas, on_delete=models.DO_NOTHING)
    Store_id = models.ForeignKey(Stores, on_delete= models.DO_NOTHING)