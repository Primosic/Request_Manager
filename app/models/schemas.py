"""
Mu00f3dulo de esquemas Pydantic para validau00e7u00e3o de requisiu00e7u00f5es e respostas da API.

Este mu00f3dulo define os esquemas Pydantic usados para validar os dados de entrada e sau00edda
da API REST do sistema de gerenciamento de solicitau00e7u00f5es de anonimizau00e7u00e3o. Os esquemas
garantem a integridade dos dados e fornecem validau00e7u00e3o automatizada.

Classes:
    RequestBase: Esquema base para solicitau00e7u00f5es de anonimizau00e7u00e3o.
    RequestCreate: Esquema para criar uma nova solicitau00e7u00e3o de anonimizau00e7u00e3o.
    RequestResponse: Esquema para resposta apu00f3s criar uma solicitau00e7u00e3o.
    VerificationRequest: Esquema para requisiu00e7u00e3o de endpoint de verificau00e7u00e3o.
    ProcessingRequest: Esquema para requisiu00e7u00e3o de atualizau00e7u00e3o de status de processamento.
    SystemStatusResponse: Esquema para status individual do sistema na resposta de status.
    StatusResponse: Esquema para resposta de consulta de status.
    AdminAdvanceRequest: Esquema para requisiu00e7u00e3o de avanu00e7o administrativo.
    ProcessProgressUpdate: Esquema para atualizau00e7u00e3o de progresso de processo.
    GenericResponse: Esquema de resposta genu00e9rica da API.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any, Union
from datetime import datetime


class RequestBase(BaseModel):
    """Base schema for anonymization request."""
    
    nm_system: str = Field(..., description="Name of the requesting system")
    id_person: str = Field(..., description="Person identification")
    tp_document: str = Field(..., description="Document type")


class RequestCreate(RequestBase):
    """Schema for creating a new anonymization request."""
    pass


class RequestResponse(BaseModel):
    """Schema for response after creating a request."""
    
    id_request: int = Field(..., description="Generated request ID")
    dt_register: datetime = Field(..., description="Registration date and time")
    nm_system: str = Field(..., description="Name of the requesting system")
    id_person: Optional[str] = Field(None, description="Person identification")
    tp_document: Optional[str] = Field(None, description="Document type")
    
    class Config:
        orm_mode = True


class VerificationRequest(BaseModel):
    """Schema for verification endpoint request."""
    
    id_request: int = Field(..., description="Request ID")
    id_system_process: int = Field(..., description="Processing system ID")
    st_system_verify: int = Field(..., description="Verification status (1=approved, 2=rejected)")
    ds_reason_verify_refuse: Optional[str] = Field(None, description="Rejection reason")
    
    @validator('st_system_verify')
    def validate_status(cls, v):
        """Validate that status is either 1 (approved) or 2 (rejected)."""
        if v not in [1, 2]:
            raise ValueError('st_system_verify must be either 1 (approved) or 2 (rejected)')
        return v
    
    @validator('ds_reason_verify_refuse')
    def validate_reason(cls, v, values):
        """Validate that reason is provided if request is rejected."""
        if 'st_system_verify' in values and values['st_system_verify'] == 2 and not v:
            raise ValueError('ds_reason_verify_refuse is required when st_system_verify=2')
        return v


class ProcessingRequest(BaseModel):
    """Schema for processing status update request."""
    
    id_request: int = Field(..., description="Request ID")
    id_system_process: int = Field(..., description="Processing system ID")
    st_system_request: int = Field(..., description="Processing status (1=completed, 3=error)")
    
    @validator('st_system_request')
    def validate_status(cls, v):
        """Validate that status is either 1 (completed) or 3 (error)."""
        if v not in [1, 3]:
            raise ValueError('st_system_request must be either 1 (completed) or 3 (error)')
        return v


class SystemStatusResponse(BaseModel):
    """Schema for individual system status in status response."""
    
    id_system_process: str = Field(..., description="System ID")
    nm_system: str = Field(..., description="System name")
    st_system_verify: int = Field(..., description="Verification status")
    st_system_request: int = Field(..., description="Processing status")
    progress_percentage: Optional[float] = Field(None, description="Completion percentage")


class StatusResponse(BaseModel):
    """Schema for status query response."""
    
    id_request: int = Field(..., description="Request ID")
    dt_register: datetime = Field(..., description="Registration date and time")
    current_status: str = Field(..., description="Overall request status")
    systems_status: List[SystemStatusResponse] = Field(..., description="Status of individual systems")


class AdminAdvanceRequest(BaseModel):
    """Schema for administrative advancement request."""
    
    admin_token: str = Field(..., description="Administrator token for authentication")
    force_status: str = Field(..., description="Status to force the request to")
    admin_note: str = Field(..., description="Justification for the advancement")


class ProcessProgressUpdate(BaseModel):
    """Schema for process progress update."""
    
    id_request: int = Field(..., description="Request ID")
    id_system_process: int = Field(..., description="Processing system ID")
    progress_percentage: float = Field(..., ge=0, le=100, description="Completion percentage")
    progress_message: Optional[str] = Field(None, description="Status message")


class GenericResponse(BaseModel):
    """Generic API response schema."""
    
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")