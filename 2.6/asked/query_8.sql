SELECT lecturers.name, AVG(grades.value) AS avg_grade
FROM lecturers
JOIN subjects ON lecturers.id = subjects.lecturer_id
JOIN grades ON subjects.id = grades.subject_id
WHERE lecturers.id = lecturer_id AND grades.subject_id = subject_id
GROUP BY lecturers.id;