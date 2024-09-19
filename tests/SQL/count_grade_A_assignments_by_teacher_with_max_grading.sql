-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH TeacherAssignmentCounts AS (
    SELECT 
        teacher_id, 
        COUNT(id) AS assignment_count
    FROM assignments
    WHERE teacher_id IS NOT NULL
    GROUP BY teacher_id
)
, TopTeacher AS (
    SELECT teacher_id
    FROM TeacherAssignmentCounts
    ORDER BY assignment_count DESC
    LIMIT 1
)
SELECT 
    COUNT(a.id) AS grade_A_count
FROM assignments a
JOIN TopTeacher tt ON a.teacher_id = tt.teacher_id
WHERE a.grade = 'A';
