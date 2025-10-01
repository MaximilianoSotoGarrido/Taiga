from typing import List, Optional, Dict
from itertools import count
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="US-01: Registro de Usuario", version="1.0.0")

class Usuario(BaseModel):
    email: str = Field(min_length=5, description="Correo del usuario")
    password: str = Field(min_length=8, description="Contraseña segura")

class UsuarioOut(Usuario):
    id: int

_db: Dict[int, Usuario] = {}
_id_seq = count(start=1)

@app.get("/health", tags=["sistema"])
def salud():
    return {"status": "200"}

@app.post("/usuarios", response_model=UsuarioOut, status_code=201)
def crear_usuario(usuario: Usuario):
    # Validación simple: email único
    if any(u.email == usuario.email for u in _db.values()):
        raise HTTPException(status_code=400, detail="Email ya registrado")
    new_id = next(_id_seq)
    _db[new_id] = usuario
    return UsuarioOut(id=new_id, **usuario.model_dump())

@app.get("/usuarios/{usuario_id}", response_model=UsuarioOut)
def obtener_usuario(usuario_id: int):
    if usuario_id not in _db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UsuarioOut(id=usuario_id, **_db[usuario_id].model_dump())
