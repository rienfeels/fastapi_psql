from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="",
    host="localhost",
    database="hillcrest_high_school",
    port=5432
)

engine = create_engine(url)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# class Student(Base):
#     __tablename__ = "students"

#     id = Column(Integer, primary_key=True)
#     name = Column(String)

# class Course(Base):
#     __tablename__ = "courses"

#     id = Column(Integer, primary_key=True)
#     name = Column(String)

# class Enrollment(Base):
#     __tablename__ = "enrollments"

#     id = Column(Integer, primary_key=True)
#     student_id = Column(Integer, ForeignKey('students.id'))
#     course_id = Column(Integer, ForeignKey('courses.id'))
#     enrollment_date = Column(Date)


Base.metadata.create_all(engine)