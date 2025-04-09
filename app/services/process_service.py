"""
Serviu00e7o para gerenciamento de processos de anonimizau00e7u00e3o.

Este mu00f3dulo contu00e9m a classe ProcessService que u00e9 responsu00e1vel por gerenciar
operau00e7u00f5es relacionadas aos processos de anonimizau00e7u00e3o de cada sistema.
Implementa operau00e7u00f5es CRUD e consulta para processos, permitindo a criação,
atualizau00e7u00e3o e monitoramento do status de processos nos diferentes sistemas.

Classe:
    ProcessService: Gerencia operau00e7u00f5es relacionadas aos processos de anonimizau00e7u00e3o.

Funu00e7u00f5es:
    create_process: Cria um novo processo para um sistema e requisiu00e7u00e3o.
    get_process: Obtu00e9m um processo pela chave composta (id_request, id_system_process).
    update_process_status: Atualiza o status de um processo.
    get_processes_by_request: Obtu00e9m todos os processos associados a uma requisiu00e7u00e3o.
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.models import Process, ProcessProgress
from app.core.notifications import NotificationService
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class ProcessService:
    """Serviu00e7o para gerenciamento de processos de anonimizau00e7u00e3o."""
    
    def __init__(self, db: Session):
        """Inicializa o serviu00e7o de processos.
        
        Args:
            db: Sessu00e3o do banco de dados
        """
        self.db = db
        self.notification_service = NotificationService()
    
    def create_process_entry(self, id_request: int, id_system_process: int, 
                             id_system_requester: int, id_person: str, tp_document: str) -> Process:
        """Cria uma nova entrada de processo para um sistema.
        
        Args:
            id_request: ID da solicitau00e7u00e3o
            id_system_process: ID do sistema de processamento
            id_system_requester: ID do sistema solicitante
            id_person: ID da pessoa
            tp_document: Tipo de documento
            
        Returns:
            Process: Entrada de processo criada
        """
        # Criar entrada de processo
        process = Process(
            id_request=id_request,
            id_system_process=id_system_process,
            id_system_requester=id_system_requester,
            id_person=id_person,
            tp_document=tp_document,
            dt_system_verify=datetime.now(),
            st_system_verify=0,  # Pendente
            st_system_request=0   # Pendente
        )
        
        self.db.add(process)
        self.db.commit()
        self.db.refresh(process)
        
        logger.info(f"Entrada de processo criada para solicitau00e7u00e3o {id_request} e sistema {id_system_process}")
        
        return process
    
    def get_process(self, id_request: int, id_system_process: int) -> Optional[Process]:
        """Obtu00e9m um processo pelo ID da solicitau00e7u00e3o e ID do sistema.
        
        Args:
            id_request: ID da solicitau00e7u00e3o
            id_system_process: ID do sistema de processamento
            
        Returns:
            Optional[Process]: O processo, se encontrado, ou None
        """
        return self.db.query(Process).filter(
            and_(
                Process.id_request == id_request,
                Process.id_system_process == id_system_process
            )
        ).first()
    
    def get_processes_for_request(self, id_request: int) -> List[Process]:
        """Obtu00e9m todos os processos para uma solicitau00e7u00e3o.
        
        Args:
            id_request: ID da solicitau00e7u00e3o
            
        Returns:
            List[Process]: Lista de processos para a solicitau00e7u00e3o
        """
        return self.db.query(Process).filter(Process.id_request == id_request).all()
    
    def update_verification_status(self, id_request: int, id_system_process: int, 
                                  st_system_verify: int, ds_reason_verify_refuse: Optional[str] = None) -> bool:
        """Atualiza o status de verificau00e7u00e3o para um processo.
        
        Args:
            id_request: ID da solicitau00e7u00e3o
            id_system_process: ID do sistema de processamento
            st_system_verify: Status de verificau00e7u00e3o
            ds_reason_verify_refuse: Motivo de recusa (se recusado)
            
        Returns:
            bool: True se atualizado, False caso contru00e1rio
        """
        # Obter processo
        process = self.get_process(id_request, id_system_process)
        if not process:
            logger.error(f"Processo nu00e3o encontrado: {id_request}, {id_system_process}")
            return False
        
        # Atualizar status de verificau00e7u00e3o
        process.st_system_verify = st_system_verify
        process.dt_system_verify_response = datetime.now()
        
        if ds_reason_verify_refuse:
            process.ds_reason_verify_refuse = ds_reason_verify_refuse
        
        self.db.commit()
        
        logger.info(f"Status de verificau00e7u00e3o atualizado para solicitau00e7u00e3o {id_request} e sistema {id_system_process}: {st_system_verify}")
        
        return True
    
    def update_processing_status(self, id_request: int, id_system_process: int, 
                               st_system_request: int) -> bool:
        """Atualiza o status de processamento para um processo.
        
        Args:
            id_request: ID da solicitau00e7u00e3o
            id_system_process: ID do sistema de processamento
            st_system_request: Status de processamento
            
        Returns:
            bool: True se atualizado, False caso contru00e1rio
        """
        # Obter processo
        process = self.get_process(id_request, id_system_process)
        if not process:
            logger.error(f"Processo nu00e3o encontrado: {id_request}, {id_system_process}")
            return False
        
        # Atualizar status de processamento
        process.st_system_request = st_system_request
        process.dt_system_conclusion = datetime.now()
        
        self.db.commit()
        
        logger.info(f"Status de processamento atualizado para solicitau00e7u00e3o {id_request} e sistema {id_system_process}: {st_system_request}")
        
        return True
    
    def update_process_progress(self, id_request: int, id_system_process: int, 
                             progress_percentage: float, progress_message: Optional[str] = None) -> bool:
        """Atualiza o progresso para um processo.
        
        Args:
            id_request: ID da solicitau00e7u00e3o
            id_system_process: ID do sistema de processamento
            progress_percentage: Porcentagem de conclusu00e3o (0-100)
            progress_message: Mensagem de progresso
            
        Returns:
            bool: True se atualizado, False caso contru00e1rio
        """
        # Verificar se o processo existe
        process = self.get_process(id_request, id_system_process)
        if not process:
            logger.error(f"Processo nu00e3o encontrado: {id_request}, {id_system_process}")
            return False
        
        # Criar entrada de progresso
        progress = ProcessProgress(
            id_request=id_request,
            id_system_process=id_system_process,
            dt_progress_update=datetime.now(),
            progress_percentage=progress_percentage,
            progress_message=progress_message
        )
        
        self.db.add(progress)
        self.db.commit()
        
        logger.info(f"Progresso atualizado para solicitau00e7u00e3o {id_request} e sistema {id_system_process}: {progress_percentage}%")
        
        return True
    
    def get_latest_progress(self, id_request: int, id_system_process: int) -> Optional[ProcessProgress]:
        """Obtu00e9m o u00faltimo progresso para um processo.
        
        Args:
            id_request: ID da solicitau00e7u00e3o
            id_system_process: ID do sistema de processamento
            
        Returns:
            Optional[ProcessProgress]: O u00faltimo progresso, se existir
        """
        return self.db.query(ProcessProgress).filter(
            and_(
                ProcessProgress.id_request == id_request,
                ProcessProgress.id_system_process == id_system_process
            )
        ).order_by(ProcessProgress.dt_progress_update.desc()).first()
    
    def get_status_text(self, status_code: int, status_type: str = "verify") -> str:
        """Converte cu00f3digo de status em representau00e7u00e3o textual.
        
        Args:
            status_code: Cu00f3digo de status
            status_type: Tipo de status ("verify" ou "request")
            
        Returns:
            str: Representau00e7u00e3o textual do status
        """
        if status_type == "verify":
            status_map = {
                0: "Pendente",
                1: "Aprovado",
                2: "Recusado",
                3: "Erro",
                4: "Timeout"
            }
        else:  # request/processing status
            status_map = {
                0: "Pendente",
                1: "Concluu00eddo",
                2: "Parcial",
                3: "Erro",
                4: "Timeout",
                5: "Cancelado"
            }
        
        return status_map.get(status_code, f"Desconhecido ({status_code})")