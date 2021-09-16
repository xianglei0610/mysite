# resources.py
from import_export import resources
from .models import User

class UserResource(resources.ModelResource):

    class Meta:
        model = User
        fields = ('id', 'name', 'telephone','age','id_card', 'remark')