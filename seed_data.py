"""
Seed database with test data
Run this after installing dependencies: python seed_data.py
"""

from database import SessionLocal, Base, engine
from models import User, Region, MMDA, ProblemCategory, Report
from auth import hash_password, generate_uuid
from datetime import datetime

def seed_database():
    """Populate database with initial test data"""
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(User).first():
            print("✅ Database already seeded. Skipping...")
            return
        
        print("🌱 Seeding database with test data...")
        
        # Create regions
        regions = [
            Region(id="region-001", name="Ashanti Region"),
            Region(id="region-002", name="Greater Accra Region"),
            Region(id="region-003", name="Eastern Region"),
        ]
        db.add_all(regions)
        db.commit()
        print("✅ Created regions")
        
        # Create MMDAs (Metropolitan, Municipal, District Assemblies)
        mmdas = [
            MMDA(id="mmda-001", name="Kumasi Metropolitan Assembly", region_id="region-001"),
            MMDA(id="mmda-002", name="Asokwa Municipal Assembly", region_id="region-001"),
            MMDA(id="mmda-003", name="Accra Metropolitan Assembly", region_id="region-002"),
            MMDA(id="mmda-004", name="Tema Metropolitan Assembly", region_id="region-002"),
            MMDA(id="mmda-005", name="Cape Coast Metropolitan Assembly", region_id="region-003"),
        ]
        db.add_all(mmdas)
        db.commit()
        print("✅ Created MMDAs")
        
        # Create problem categories
        categories = [
            ProblemCategory(id="cat-001", name="Roads & Infrastructure"),
            ProblemCategory(id="cat-002", name="Water & Sanitation"),
            ProblemCategory(id="cat-003", name="Electricity"),
            ProblemCategory(id="cat-004", name="Waste Management"),
            ProblemCategory(id="cat-005", name="Education"),
            ProblemCategory(id="cat-006", name="Health"),
            ProblemCategory(id="cat-007", name="Security"),
            ProblemCategory(id="cat-008", name="Other"),
        ]
        db.add_all(categories)
        db.commit()
        print("✅ Created problem categories")
        
        # Create test users
        users = [
            User(
                id=generate_uuid(),
                email="citizen@example.com",
                display_name="John Doe",
                phone="+233123456789",
                hashed_password=hash_password("password123"),
                role="citizen",
                region="region-001",
                is_active=True
            ),
            User(
                id=generate_uuid(),
                email="minister@example.com",
                display_name="Hon. Jane Smith",
                phone="+233987654321",
                hashed_password=hash_password("password123"),
                role="minister",
                region="region-001",
                is_active=True
            ),
            User(
                id=generate_uuid(),
                email="official@example.com",
                display_name="Mr. Peter Mensah",
                phone="+233555555555",
                hashed_password=hash_password("password123"),
                role="glinax",
                region="region-001",
                is_active=True
            ),
        ]
        db.add_all(users)
        db.commit()
        print("✅ Created test users")
        print("   - Citizen: citizen@example.com / password123")
        print("   - Minister: minister@example.com / password123")
        print("   - Official: official@example.com / password123")
        
        # Create sample reports
        citizen_user = db.query(User).filter(User.email == "citizen@example.com").first()
        
        if citizen_user:
            reports = [
                Report(
                    id=generate_uuid(),
                    user_id=citizen_user.id,
                    region="region-001",
                    mmda="mmda-001",
                    community="Asawase",
                    category="Roads & Infrastructure",
                    title="Pothole on Adum Road",
                    description="There is a large pothole on Adum Road near the market that is dangerous for vehicles and pedestrians.",
                    severity="high",
                    ghana_postgps="AS-001-0001",
                    status="pending"
                ),
                Report(
                    id=generate_uuid(),
                    user_id=citizen_user.id,
                    region="region-001",
                    mmda="mmda-001",
                    community="Kwadaso",
                    category="Water & Sanitation",
                    title="Water shortage in Kwadaso",
                    description="The community has been without water for 3 weeks. We need urgent attention.",
                    severity="high",
                    status="in_progress"
                ),
                Report(
                    id=generate_uuid(),
                    user_id=citizen_user.id,
                    region="region-001",
                    mmda="mmda-001",
                    community="Tafo",
                    category="Electricity",
                    title="Street lights not working",
                    description="Most street lights in Tafo have not been working for 2 months.",
                    severity="medium",
                    status="pending"
                ),
            ]
            db.add_all(reports)
            db.commit()
            print("✅ Created sample reports")
        
        print("🌱 Database seeding completed successfully!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
