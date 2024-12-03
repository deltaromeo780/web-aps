SELECT groups.name, AVG(grades.value) AS avg_grade
FROM students
JOIN groups ON students.group_id = groups.id
JOIN grades ON students.id = grades.student_id
WHERE grades.subject_id = subject_id
GROUP BY groups.id;