-- Write query to get number of graded assignments for each student:
SELECT 
    s.id AS student_id, 
    COUNT(a.id) AS graded_assignments_count
FROM students s
LEFT JOIN assignments a ON s.id = a.student_id
GROUP BY s.id;

