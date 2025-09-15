"""Contract model for labor contracts"""

from sqlalchemy import Column, String, Date, ForeignKey, Text, Enum, Float, Integer, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import enum

from app.models.base import BaseModel


class ContractType(enum.Enum):
    """Contract type enum - Loại hợp đồng"""
    PROBATION = "PROBATION"  # Thử việc
    FIXED_TERM_12 = "FIXED_TERM_12"  # Xác định thời hạn 12 tháng
    FIXED_TERM_24 = "FIXED_TERM_24"  # Xác định thời hạn 24 tháng
    FIXED_TERM_36 = "FIXED_TERM_36"  # Xác định thời hạn 36 tháng
    INDEFINITE = "INDEFINITE"  # Không xác định thời hạn
    SEASONAL = "SEASONAL"  # Theo mùa vụ
    PART_TIME = "PART_TIME"  # Làm việc không trọn thời gian


class ContractStatus(enum.Enum):
    """Contract status enum"""
    DRAFT = "DRAFT"  # Nháp
    ACTIVE = "ACTIVE"  # Đang hiệu lực
    EXPIRED = "EXPIRED"  # Hết hạn
    TERMINATED = "TERMINATED"  # Chấm dứt
    EXTENDED = "EXTENDED"  # Đã gia hạn
    SUSPENDED = "SUSPENDED"  # Tạm hoãn


class Contract(BaseModel):
    """Contract model - Hợp đồng lao động"""
    
    __tablename__ = "contracts"
    
    # Basic information
    contract_number = Column(String(100), unique=True, nullable=False, index=True)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=False)
    
    # Contract type and status
    contract_type = Column(Enum(ContractType), nullable=False)
    status = Column(Enum(ContractStatus), default=ContractStatus.DRAFT, nullable=False)
    
    # Contract duration
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)  # Null for indefinite contracts
    probation_end_date = Column(Date, nullable=True)  # Ngày kết thúc thử việc
    
    # Contract order
    contract_order = Column(Integer, default=1)  # Hợp đồng lần thứ mấy
    previous_contract_id = Column(UUID(as_uuid=True), ForeignKey("contracts.id"), nullable=True)
    
    # Salary information
    basic_salary = Column(Float, nullable=False)
    salary_coefficient = Column(Float)
    allowances = Column(Float, default=0)
    
    # Work information
    position = Column(String(255))
    department = Column(String(255))
    work_location = Column(String(500))
    job_description = Column(Text)
    
    # Signing information
    signed_date = Column(Date)
    signed_by_employee = Column(Boolean, default=False)
    signed_by_employer = Column(Boolean, default=False)
    employer_representative = Column(String(255))  # Người đại diện bên sử dụng lao động
    
    # Files
    contract_file_url = Column(String(500))  # Link to contract file
    appendix_file_url = Column(String(500))  # Link to appendix file
    
    # Termination information
    termination_date = Column(Date)
    termination_reason = Column(Text)
    termination_decision_number = Column(String(100))
    
    # Extension information
    extended_to_contract_id = Column(UUID(as_uuid=True), ForeignKey("contracts.id"), nullable=True)
    extension_reason = Column(Text)
    
    # Warning flags
    probation_warning_sent = Column(Boolean, default=False)
    expiry_warning_sent = Column(Boolean, default=False)
    
    # Notes
    notes = Column(Text)
    
    # Relationships
    employee = relationship("Employee", back_populates="contracts")
    previous_contract = relationship("Contract", remote_side="Contract.id", foreign_keys=[previous_contract_id])
    extended_contract = relationship("Contract", remote_side="Contract.id", foreign_keys=[extended_to_contract_id])
    
    def __repr__(self):
        return f"<Contract {self.contract_number}: {self.employee_id}>">