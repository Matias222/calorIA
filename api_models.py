from collections import deque
from datetime import datetime
from typing import Literal

import pytz
from fastapi import WebSocket
from pydantic import BaseModel, Field

class ApiState(BaseModel):

    class Config: 
        arbitrary_types_allowed = True


    buffer: list | None = Field(default=[])
    estado_conversa: str | None = Field(default="Onboarding")
    respuesta_usuario: str | None = Field(default="Default")
    json_onboarding: map | None = Field(default={})
    numero_enviar: str | None = Field(default="")
    limite_calorias_diarias: float | None = Field(default=0.0)
    nombre: str | None = Field(default="")