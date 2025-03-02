from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from apps.estimate_funnel.routers.input_router import router as input_router

api = NinjaAPI()


api.add_router("/input/", input_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
