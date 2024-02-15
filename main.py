from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import session 
from models import Students, Courses, Enrollments

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/create/student")
async def create_student(name: str):
    student = Students(name=name)
    session.add(student)
    session.commit()
    return {"Student created": student.name}

@app.post("/create/course")
async def create_course(name: str):
    course = Courses(name=name)
    session.add(course)
    session.commit()
    return {"Course created": course.name}

@app.post("/create/enrollment")
async def create_enrollment(student_id: int, course_id: int):
    enrollment = Enrollments(student_id=student_id, course_id=course_id)
    session.add(enrollment)
    session.commit()
    return {"Enrollment created": f"Student {student_id} enrolled in Course {course_id}"}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the school management system"}

@app.get("/students")
async def read_students():
    students = session.query(Students)
    return students.all()

@app.get("/courses")
async def read_courses():
    courses = session.query(Courses)
    return courses.all()

@app.get("/enrollment")
async def read_enrollment():
    enrollments = session.query(Enrollments, Students, Courses).join(Students, Students.id == Enrollments.student_id).join(Courses, Courses.id == Enrollments.course_id)
    results = enrollments.all()
    enrollment_list = []
    for enrollments in results:
        enrollment_dict = {
            "enrollment_id": enrollments.Enrollments.enrollment_id,
            "student_name": enrollments.Students.name,
            "course_name": enrollments.Courses.name,
            "enrollment_date": enrollments.Enrollments.enrollment_date
        }
        enrollment_list.append(enrollment_dict)
    return enrollment_list

@app.put("/update/student/{id}")
async def update_student(id: int, name: str):
    student = session.query(Students).filter(Students.id == id).first()
    if student:
        student.name = name
        session.commit()
        return {"Updated student": student.name}
    else:
        return {"message": "Student not found"}
    
@app.put("/update/course/{id}")
async def update_course(id: int, name: str):
    course = session.query(Courses).filter(Courses.id == id).first()
    if course:
        course.name = name
        session.commit()
        return {"Updated course": course.name}
    else:
        return {"message": "Course not found"}
    
@app.put("/update/enrollment/{id}")
async def update_enrollment(id: int, student_id: int, course_id: int):
    enrollment = session.query(Enrollments).filter(Enrollments.id == id).first()
    if enrollment:
        enrollment.student_id = student_id
        enrollment.course_id = course_id
        session.commit()
        return {"Updated enrollment": f"Student {student_id} enrolled in Course {course_id}"}
    else:
        return {"message": "Enrollment not found"}
    
@app.delete("/delete/student/{id}")
async def delete_student(id: int):
    student = session.query(Students).filter(Students.id == id).first()
    if student:
        session.delete(student)
        session.commit()
        return {"Deleted student": student.name}
    else:
        return {"message": "Student not found"}
    
@app.delete("/delete/course/{id}")
async def delete_course(id: int):
    course = session.query(course).filter(Courses.id == id).first()
    if course:
        session.delete(course)
        session.commit()
        return {"Deleted course": course.name}
    else:
        return {"message": "Course not found"}
    
@app.delete("/delete/enrollment/{id}")
async def delete_enrollment(id: int):
    enrollment = session.query(Enrollments).filter(Enrollments.id == id).first()
    if enrollment:
        session.delete(enrollment)
        session.commit()
        return {"Deleted enrollment": f"Student {enrollment.student_id} enrolled in Course {enrollment.course_id}"}
    else:
        return {"message": "Enrollment not found"}
