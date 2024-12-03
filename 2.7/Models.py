from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship



Base = declarative_base()


class Groups(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    students = relationship('Students', back_populates='group')


class Students(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship('Groups', back_populates='students')
    grades = relationship('Grades', back_populates='student')


class Lecturers(Base):
    __tablename__ = 'lecturers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    subjects = relationship('Subjects', back_populates='lecturer')


class Subjects(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    lecturer_id = Column(Integer, ForeignKey('lecturers.id'))
    lecturer = relationship('Lecturers', back_populates='subjects')
    grades = relationship('Grades', back_populates='subject')


class Grades(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    value = Column(Integer)
    date = Column(Date)
    student = relationship('Students', back_populates='grades')
    subject = relationship('Subjects', back_populates='grades')