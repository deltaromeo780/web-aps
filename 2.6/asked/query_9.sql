SELECT DISTINCT subjects.name
FROM subjects
JOIN grades ON subjects.id = grades.subject_id
WHERE grades.student_id = student_id;