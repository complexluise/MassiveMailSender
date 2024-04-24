from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class Contact(BaseModel):
    """Contact from Oriflame Network"""
    codigo: str = Field(..., alias='Codigo')
    nombre: str = Field(..., alias='Nombre')
    ciudad_departamento: str = Field(..., alias='Ciudad-Departamento')
    barrio: str = Field(..., alias='Barrio')
    email: EmailStr = Field(..., alias='Email')
    telefono: str = Field(..., alias='Telefono')
    catalogo_reclutado: str = Field(..., alias='Catalogo Reclutado')
    puntos_c03_2024: int = Field(..., alias='Puntos\n C03-2024')
    puntos_c04_2024: int = Field(..., alias='Puntos\n C04-2024')
    puntos_c05_2024: int = Field(..., alias='Puntos\n C05-2024')
    puntos_c06_2024: int = Field(..., alias='Puntos\n C06-2024')
    status_c05_2024: Optional[str] = Field(None, alias='Status\n C05-2024')
    nuevo_nivel_c05_2024: Optional[str] = Field(None, alias='Nuevo Nivel\n C05-2024')
    status_c06_2024: Optional[str] = Field(None, alias='Status\n C06-2024')
    pushed_c06_2024: Optional[str] = Field(None, alias='Pushed\n C06-2024')
    recluta_c06_2024: Optional[str] = Field(None, alias='Recluta\n C06-2024')
    cupo_disponible: str = Field(..., alias='Cupo Disponible')
    descripcion_credito: Optional[str] = Field(None, alias='Descripcion Credito')
    deuda: Optional[int] = Field(None, alias='Deuda')
    # Add other fields as necessary based on the continuation of the headers...
