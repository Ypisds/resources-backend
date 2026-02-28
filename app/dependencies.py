from typing import Annotated
from .services.resources_service import ResourceService

def get_resource_service() -> ResourceService:
    return ResourceService(name="Nome qualquer")