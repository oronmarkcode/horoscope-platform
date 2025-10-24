"""Initialize database with sample data."""

from datetime import date
from sqlalchemy.orm import Session

from horoscope_backend.core.database import SessionLocal, engine
from horoscope_backend.core.database import Base
from horoscope_backend.models.horoscope import Horoscope

# Create all tables
Base.metadata.create_all(bind=engine)

# Create sample data
def create_sample_data():
    """Create sample horoscope data."""
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Horoscope).first():
            print("Sample data already exists")
            return
        
        # Create sample horoscopes
        sample_horoscopes = [
            Horoscope(
                sign="Aries",
                date=date.today(),
                content="Today is a great day for new beginnings. Trust your instincts and take action on your goals.",
                author="AstroBot"
            ),
            Horoscope(
                sign="Taurus",
                date=date.today(),
                content="Focus on stability and security today. Your practical approach will lead to success.",
                author="AstroBot"
            ),
            Horoscope(
                sign="Gemini",
                date=date.today(),
                content="Communication is key today. Share your ideas and listen to others' perspectives.",
                author="AstroBot"
            ),
            Horoscope(
                sign="Cancer",
                date=date.today(),
                content="Trust your emotions today. They are guiding you in the right direction.",
                author="AstroBot"
            ),
            Horoscope(
                sign="Leo",
                date=date.today(),
                content="Your natural leadership qualities will shine today. Take center stage.",
                author="AstroBot"
            ),
            Horoscope(
                sign="Virgo",
                date=date.today(),
                content="Attention to detail will serve you well today. Don't rush through important tasks.",
                author="AstroBot"
            ),
            Horoscope(
                sign="Libra",
                date=date.today(),
                content="Balance and harmony are your strengths today. Seek compromise in conflicts.",
                author="AstroBot"
            ),
            Horoscope(
                sign="Scorpio",
                date=date.today(),
                content="Your intensity and passion will help you overcome obstacles today.",
                author="AstroBot"
            ),
            Horoscope(
                sign="Sagittarius",
                date=date.today(),
                content="Adventure and exploration call to you today. Embrace new experiences.",
                author="AstroBot"
            ),
            Horoscope(
                sign="Capricorn",
                date=date.today(),
                content="Your hard work and determination will pay off today. Stay focused on your goals.",
                author="AstroBot"
            ),
            Horoscope(
                sign="Aquarius",
                date=date.today(),
                content="Innovation and originality are your strengths today. Think outside the box.",
                author="AstroBot"
            ),
            Horoscope(
                sign="Pisces",
                date=date.today(),
                content="Your intuition and creativity will guide you today. Trust your inner voice.",
                author="AstroBot"
            ),
        ]
        
        for horoscope in sample_horoscopes:
            db.add(horoscope)
        
        db.commit()
        print("Sample data created successfully")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_sample_data()
