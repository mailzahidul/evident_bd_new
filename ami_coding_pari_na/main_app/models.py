from django.db import models
from user_admin.models import User

# Create your models here.


class InputValue(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    input_values = models.CharField(max_length=255)
