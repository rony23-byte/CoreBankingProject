
from django.urls import path,re_path
from rest_framework import routers
from mayerapi.views import LoanViewSets,ClientViewSet,schema_view
router=routers.DefaultRouter()
router.register('loans',LoanViewSets)
router.register('clients',ClientViewSet)
urlpatterns=router.urls
urlpatterns+=[
    re_path(r'^swagger(?P<format>\.json\yaml)$',
    schema_view.without_ui(cache_timeout=0),
    name='schema-json'

    ),
    path(
        'swagger/',
        schema_view.with_ui('swagger',cache_timeout=0),
        name='schema-swagger-ui'
    ),
]
 