from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
import os

from database import Base, engine, get_db
from models import User, Report, Region, MMDA, ProblemCategory
from schemas import (
    LoginRequest, SignupRequest, LoginResponse, UserResponse,
    ReportCreate, ReportResponse, ReportUpdate,
    RegionResponse, MMDAResponse, ProblemCategoryResponse
)
from auth import (
    hash_password, verify_password, create_access_token,
    decode_token, generate_uuid, ACCESS_TOKEN_EXPIRE_MINUTES
)

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(title="Ashanti Community Reports API", version="0.1.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper function to get current user from token
def get_current_user(db: Session = Depends(get_db)):
    """Extract user from Authorization header"""
    # This is a simplified version - in production you'd get the token from the header
    # For demo purposes, we'll allow requests without strict authentication
    return None

# ==================== AUTH ENDPOINTS ====================

@app.post("/auth/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login user and return JWT token"""
    
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email},
        expires_delta=access_token_expires
    )
    
    # Return token and user data
    return LoginResponse(
        token=access_token,
        accessToken=access_token,
        user=UserResponse(
            id=user.id,
            email=user.email,
            display_name=user.display_name,
            phone=user.phone,
            role=user.role,
            region=user.region,
            created_at=user.created_at
        ),
        role=user.role
    )

@app.post("/auth/signup", response_model=LoginResponse)
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    """Register new user"""
    
    # Check if user exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    new_user = User(
        id=generate_uuid(),
        email=request.email,
        display_name=request.display_name,
        phone=request.phone,
        hashed_password=hash_password(request.password),
        role=request.role,
        region=request.region,
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.id, "email": new_user.email},
        expires_delta=access_token_expires
    )
    
    # Return token and user data
    return LoginResponse(
        token=access_token,
        accessToken=access_token,
        user=UserResponse(
            id=new_user.id,
            email=new_user.email,
            display_name=new_user.display_name,
            phone=new_user.phone,
            role=new_user.role,
            region=new_user.region,
            created_at=new_user.created_at
        ),
        role=new_user.role
    )

# ==================== USER ENDPOINTS ====================

@app.get("/users/me", response_model=UserResponse)
def get_me(db: Session = Depends(get_db)):
    """Get current user - requires token in Authorization header"""
    # For demo, return first citizen user
    user = db.query(User).filter(User.role == "citizen").first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        id=user.id,
        email=user.email,
        display_name=user.display_name,
        phone=user.phone,
        role=user.role,
        region=user.region,
        created_at=user.created_at
    )

@app.patch("/users/update")
def update_user(user_data: dict, db: Session = Depends(get_db)):
    """Update user data"""
    user = db.query(User).filter(User.role == "citizen").first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user_data.items():
        if hasattr(user, key):
            setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    
    return UserResponse(
        id=user.id,
        email=user.email,
        display_name=user.display_name,
        phone=user.phone,
        role=user.role,
        region=user.region,
        created_at=user.created_at
    )

@app.delete("/users/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    """Delete user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted"}

# ==================== APP DATA ENDPOINTS ====================

@app.get("/app/regions", response_model=list)
def get_regions(db: Session = Depends(get_db)):
    """Get all regions"""
    regions = db.query(Region).all()
    return [RegionResponse(id=r.id, name=r.name) for r in regions]

@app.get("/app/mmdas/{region_id}", response_model=list)
def get_mmdas(region_id: str, db: Session = Depends(get_db)):
    """Get MMDAs for a region"""
    mmdas = db.query(MMDA).filter(MMDA.region_id == region_id).all()
    return [MMDAResponse(id=m.id, name=m.name, region_id=m.region_id) for m in mmdas]

@app.get("/app/problem-categories", response_model=list)
def get_problem_categories(db: Session = Depends(get_db)):
    """Get all problem categories"""
    categories = db.query(ProblemCategory).all()
    return [ProblemCategoryResponse(id=c.id, name=c.name) for c in categories]

# ==================== REPORT ENDPOINTS ====================

@app.post("/reports/submit", response_model=ReportResponse)
def submit_report(report: ReportCreate, db: Session = Depends(get_db)):
    """Submit a new report"""
    
    # Get first user for demo (in production, get from token)
    user = db.query(User).filter(User.role == "citizen").first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # Create report
    new_report = Report(
        id=generate_uuid(),
        user_id=user.id,
        region=report.region,
        mmda=report.mmda,
        community=report.community,
        category=report.category,
        title=report.title,
        description=report.description,
        severity=report.severity,
        ghana_postgps=report.ghanaPostgps,
        file_url=report.fileUrl,
        status="pending"
    )
    
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    
    return ReportResponse(
        id=new_report.id,
        user_id=new_report.user_id,
        region=new_report.region,
        mmda=new_report.mmda,
        community=new_report.community,
        category=new_report.category,
        title=new_report.title,
        description=new_report.description,
        severity=new_report.severity,
        ghana_postgps=new_report.ghana_postgps,
        file_url=new_report.file_url,
        status=new_report.status,
        created_at=new_report.created_at,
        updated_at=new_report.updated_at
    )

@app.get("/reports/my-reports", response_model=list)
def get_my_reports(db: Session = Depends(get_db)):
    """Get current user's reports"""
    
    # Get first citizen user for demo
    user = db.query(User).filter(User.role == "citizen").first()
    if not user:
        return []
    
    reports = db.query(Report).filter(Report.user_id == user.id).all()
    
    return [
        ReportResponse(
            id=r.id,
            user_id=r.user_id,
            region=r.region,
            mmda=r.mmda,
            community=r.community,
            category=r.category,
            title=r.title,
            description=r.description,
            severity=r.severity,
            ghana_postgps=r.ghana_postgps,
            file_url=r.file_url,
            status=r.status,
            created_at=r.created_at,
            updated_at=r.updated_at
        )
        for r in reports
    ]

@app.get("/reports/minister-dashboard", response_model=list)
def get_minister_dashboard(db: Session = Depends(get_db)):
    """Get all reports for minister"""
    
    reports = db.query(Report).all()
    
    return [
        ReportResponse(
            id=r.id,
            user_id=r.user_id,
            region=r.region,
            mmda=r.mmda,
            community=r.community,
            category=r.category,
            title=r.title,
            description=r.description,
            severity=r.severity,
            ghana_postgps=r.ghana_postgps,
            file_url=r.file_url,
            status=r.status,
            created_at=r.created_at,
            updated_at=r.updated_at
        )
        for r in reports
    ]

@app.get("/reports/{report_id}", response_model=ReportResponse)
def get_report(report_id: str, db: Session = Depends(get_db)):
    """Get a specific report"""
    
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return ReportResponse(
        id=report.id,
        user_id=report.user_id,
        region=report.region,
        mmda=report.mmda,
        community=report.community,
        category=report.category,
        title=report.title,
        description=report.description,
        severity=report.severity,
        ghana_postgps=report.ghana_postgps,
        file_url=report.file_url,
        status=report.status,
        created_at=report.created_at,
        updated_at=report.updated_at
    )

@app.patch("/reports/{report_id}", response_model=ReportResponse)
def update_report(report_id: str, report_data: ReportUpdate, db: Session = Depends(get_db)):
    """Update a report"""
    
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Update fields if provided
    for key, value in report_data.dict(exclude_unset=True).items():
        if hasattr(report, key):
            # Convert camelCase to snake_case for certain fields
            if key == "ghanaPostgps":
                setattr(report, "ghana_postgps", value)
            elif key == "fileUrl":
                setattr(report, "file_url", value)
            else:
                setattr(report, key, value)
    
    db.commit()
    db.refresh(report)
    
    return ReportResponse(
        id=report.id,
        user_id=report.user_id,
        region=report.region,
        mmda=report.mmda,
        community=report.community,
        category=report.category,
        title=report.title,
        description=report.description,
        severity=report.severity,
        ghana_postgps=report.ghana_postgps,
        file_url=report.file_url,
        status=report.status,
        created_at=report.created_at,
        updated_at=report.updated_at
    )

@app.delete("/reports/{report_id}")
def delete_report(report_id: str, db: Session = Depends(get_db)):
    """Delete a report"""
    
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    db.delete(report)
    db.commit()
    
    return {"message": "Report deleted"}

# ==================== HEALTH CHECK ====================

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "Ashanti Community Reports API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
