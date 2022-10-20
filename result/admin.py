from django.contrib import admin

from .models import Result, Score, Token
# Register your models here.


admin.site.register(Result)
admin.site.register(Token)
admin.site.register(Score)
