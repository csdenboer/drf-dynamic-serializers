from django.apps import AppConfig

# ensure app settings are loaded
from drf_dynamic_serializers.conf import settings


class DRFDynamicSerializersConfig(AppConfig):
    name = "drf_dynamic_serializers"
    verbose_name = "DRF Dynamic Serializers"
