SELECT DISTINCT subjects.name
FROM subjects
JOIN grades ON subjects.id = grades.subject_id
JOIN lecturers ON subjects.lecturer_id = lecturers.id
WHERE lecturers.id = lecturer_id AND grades.student_id = student_id;