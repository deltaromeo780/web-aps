SELECT students.name, subjects.name, grades.value
FROM students
JOIN grades ON students.id = grades.student_id
JOIN subjects ON grades.subject_id = subjects.id
WHERE students.group_id = group_id AND grades.subject_id = subject_id;