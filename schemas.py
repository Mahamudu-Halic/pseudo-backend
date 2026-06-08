from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

# Region
class RegionBase(BaseModel):
    id: str
    name: str

class RegionResponse(RegionBase):
    class Config:
        from_attributes = True

# MMDA
class MMDABase(BaseModel):
    id: str
    name: str
    region_id: str

class MMDAResponse(MMDABase):
    class Config:
        from_attributes = True

# Problem Category
class ProblemCategoryBase(BaseModel):
    id: str
    name: str

class ProblemCategoryResponse(ProblemCategoryBase):
    class Config:
        from_attributes = True

# Auth
class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    email: str
    password: str
    display_name: str = Field(alias="displayName")
    phone: str
    region: str
    role: str = "citizen"
    
    model_config = ConfigDict(populate_by_name=True)

# User
class UserBase(BaseModel):
    id: str
    email: str
    display_name: str
    phone: str
    role: str
    region: Optional[str] = None
    created_at: datetime

class UserResponse(UserBase):
    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    token: str
    accessToken: str
    user: UserResponse
    role: str

# Report
class ReportBase(BaseModel):
    region: str
    mmda: str
    community: Optional[str] = None
    category: str
    title: str
    description: str
    severity: str
    ghana_postgps: Optional[str] = Field(None, alias="ghanaPostgps")
    file_url: Optional[str] = Field(None, alias="fileUrl")
    
    model_config = ConfigDict(populate_by_name=True)

class ReportCreate(ReportBase):
    pass

class ReportUpdate(BaseModel):
    region: Optional[str] = None
    mmda: Optional[str] = None
    community: Optional[str] = None
    category: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    ghana_postgps: Optional[str] = Field(None, alias="ghanaPostgps")
    file_url: Optional[str] = Field(None, alias="fileUrl")
    status: Optional[str] = None
    
    model_config = ConfigDict(populate_by_name=True)

class ReportResponse(BaseModel):
    id: str
    user_id: str
    region: str
    mmda: str
    community: Optional[str]
    category: str
    title: str
    description: str
    severity: str
    ghana_postgps: Optional[str]
    file_url: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
