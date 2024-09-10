from collections import deque
from datetime import datetime
from typing import Literal
from fastapi import WebSocket, BackgroundTasks
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
    background_tasks: BackgroundTasks
    nacimiento: str | None
    objetivo: str | None
    peso: float | None

class Recordatorio(BaseModel):
    numero: str
    mensaje: str