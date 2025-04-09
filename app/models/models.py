"""
Database models module.

Este mu00f3dulo define os modelos SQLAlchemy ORM para todas as tabelas do banco de dados.
Ele fornece as estruturas de dados necessu00e1rias para interagir com o banco de dados SQL Server
usado no sistema de gerenciamento de solicitau00e7u00f5es de anonimizau00e7u00e3o.

Classes:
    Request: Modelo para rastrear solicitau00e7u00f5es de anonimizau00e7u00e3o recebidas dos sistemas.
    DomSystem: Modelo para tabela de referu00eancia de domu00ednio do sistema.
    Process: Modelo para armazenar informau00e7u00f5es de status de processamento com chave primu00e1ria composta.
    ProcessProgress: Modelo para armazenar informau00e7u00f5es de progresso de processamento.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text, Float, PrimaryKeyConstraint
from sqlalchemy.sql import func
from app.db.database import Base
from datetime import datetime


class Request(Base):
    """Request table model for tracking anonymization requests received from systems."""
    __tablename__ = "tb_request"

    id_request = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dt_register = Column(DateTime, default=func.now(), nullable=False)
    ct_payload = Column(JSON, nullable=False)
    nm_system = Column(String(100), nullable=False)
    
    def __repr__(self):
        return f"<Request id_request={self.id_request}, nm_system={self.nm_system}>"


class DomSystem(Base):
    """Model for system domain reference table."""

    __tablename__ = "tb_dom_system"

    id_dom_system = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nm_system = Column(String(100), nullable=False, unique=True)
    system_type = Column(String(20), nullable=False)  # 'process' or 'requester'
    api_verify_address = Column(String(255))
    api_request_address = Column(String(255))  # Endereu00e7o para solicitau00e7u00f5es de processamento
    api_status_address = Column(String(255))
    verification_timeout_days = Column(Integer, default=7)
    processing_timeout_days = Column(Integer, default=30)
    max_retry_attempts = Column(Integer, default=5)
    
    def __repr__(self):
        return f"<DomSystem(id={self.id_dom_system}, name={self.nm_system}, type={self.system_type})>"


class Process(Base):
    """Model for storing processing status information."""

    __tablename__ = "tb_process"

    # Chave primu00e1ria composta (sem id_process u00fanico)
    id_request = Column(Integer, nullable=False)
    id_system_process = Column(Integer, nullable=False)
    
    # Definiu00e7u00e3o explu00edcita da chave primu00e1ria composta
    __table_args__ = (
        PrimaryKeyConstraint('id_request', 'id_system_process'),
    )
    
    # Outros campos
    id_system_requester = Column(Integer, nullable=True)
    dt_system_verify = Column(DateTime, nullable=True)
    dt_system_verify_response = Column(DateTime, nullable=True)
    dt_system_request = Column(DateTime, nullable=True)
    dt_system_conclusion = Column(DateTime, nullable=True)
    id_person = Column(String(100), nullable=True)
    tp_document = Column(String(20), nullable=True)  # Ajustado para nvarchar(20)
    st_system_verify = Column(Integer, default=0, nullable=True)  # 0=pending, 1=approved, 2=rejected, 3=error, 4=timeout
    ds_reason_verify_refuse = Column(String(500), nullable=True)  # Ajustado para nvarchar(500)
    st_system_request = Column(Integer, default=0, nullable=True)  # 0=pending, 1=completed, 2=partial, 3=error, 4=timeout, 5=canceled
    st_system_process = Column(Integer, nullable=True)  # 1=responded, 3=response error
    
    def __repr__(self):
        return f"<Process(id_request={self.id_request}, id_system_process={self.id_system_process})>"


class ProcessProgress(Base):
    """Model for storing processing progress information."""

    __tablename__ = "tb_process_progress"

    id_process_progress = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_request = Column(Integer, nullable=False, index=True)
    id_system_process = Column(Integer, nullable=False)
    dt_progress_update = Column(DateTime, default=func.now(), nullable=False)
    progress_percentage = Column(Float, nullable=False, default=0.0)
    progress_message = Column(Text)
    
    def __repr__(self):
        return f"<ProcessProgress(id_request={self.id_request}, percentage={self.progress_percentage})>"