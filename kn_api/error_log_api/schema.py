#import graphene
from graphene import String,Int,ObjectType,ID,Field,Schema
from graphene_django.types import DjangoObjectType
from .models import ErrorLog as ErrorLogModel  # Import your Django model

# Define the GraphQL type for ErrorLog
class ErrorLog(ObjectType):
    id = String()
    user_id = Int()
    error_type = String()
    message = String()
    created_at = String()
    updated_at = String()
class ErrorLog(DjangoObjectType):
    class Meta:
        model = ErrorLogModel  # Specify the Django model
        fields = '__all__'

# Define the Query class with resolver functions
class Query(ObjectType):
    get_error_log = Field(ErrorLog, id=ID())

    def resolve_get_error_log(self, info, id):
        # Implement your resolver logic here
        # For example, return a dummy error log
        return {
            'id': 1,
            'user_id': 1,
            'error_type': 'Runtime Error',
            'message': 'Division by zero',
            'created_at': '2024-03-27T18:00:41.384186Z',
            'updated_at': '2024-03-27T18:00:41.384186Z'
        }

schema = Schema(query=Query)