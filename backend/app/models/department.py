"""Department and Position models"""

from sqlalchemy import Column, String, Text, ForeignKey, Integer, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import BaseModel


class Department(BaseModel):
    """Department model - Phòng ban/Đơn vị"""
    
    __tablename__ = "departments"
    
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=True)
    manager_id = Column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=True)
    order = Column(Integer, default=0)
    
    # Relationships
    employees = relationship("Employee", back_populates="department")
    children = relationship("Department", backref="parent", remote_side="Department.id")
    
    def __repr__(self):
        return f"<Department {self.code}: {self.name}>"


class Position(BaseModel):
    """Position model - Chức vụ/Chức danh"""
    
    __tablename__ = "positions"
    
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    level = Column(Integer)  # Cấp bậc
    order = Column(Integer, default=0)
    
    # Allowances - Phụ cấp
    position_allowance = Column(Float, default=0)  # Phụ cấp chức vụ
    responsibility_allowance = Column(Float, default=0)  # Phụ cấp trách nhiệm
    
    # Special flags
    is_leadership = Column(Boolean, default=False)  # Là chức vụ lãnh đạo
    is_management = Column(Boolean, default=False)  # Là chức vụ quản lý
    is_executive_committee = Column(Boolean, default=False)  # Ủy viên BCH
    is_presidium_member = Column(Boolean, default=False)  # Ủy viên Đoàn Chủ tịch
    
    # Relationships
    employees = relationship("Employee", back_populates="position")
    
    def __repr__(self):
        return f"<Position {self.code}: {self.name}>">