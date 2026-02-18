admin
admin123
* Study Time (1–4)
How many hours the student studies per week (category):
Value        Meaning
1        Very low study time (< 2 hours/week)
2        Low study time (2–5 hours/week)
3        Medium study time (5–10 hours/week)
4        High study time (> 10 hours/week)

* Past Failures (0–3)
Number of past class failures.
Value        Meaning
0        No failures
1        Failed once
2        Failed twice
3        Failed three or more times
Higher failures usually → lower future performance.

* Absences
Total number of school days the student missed.
Example:
0 → perfect attendance
10 → missed 10 days
30 → missed 30 days
More absences → worse performance generally.

* Health (1–5)
Student's self-reported health condition:
Value        Meaning
1        Very poor
2        Poor
3        Average
4        Good
5        Excellent
Better health often supports better study consistency.

* First Period Grade (G1) (0–20)
Marks scored in the first internal exam / term.
Range:
            0 (fail) → 20 (excellent)

* Second Period Grade (G2) (0–20)
Marks scored in the second internal exam / term.
Also:
       0 → 20 G1 and G2 are strong predictors of final grade (G3).

Why these features matter for ML
Your model uses them because:


Feature                Effect
Study Time	Improves understanding
Failures	Indicates learning difficulty
Absences	Reduces classroom exposure
Health   	Affects focus & consistency
G1, G2	        Shows past academic ability
	

Report-ready definition (you can copy)
The dataset includes academic and behavioral attributes such as study time, past failures, absences, health condition, and previous term grades (G1 and G2). These features were selected due to their strong influence on students’ final academic performance.