
def cal_score():
    for i in new_scores:
        if i >= best - 10:
            grade.append('A')
        elif i >= best - 20:
            grade.append('B')
        elif i >= best - 30:
            grade.append('C')
        elif i >= best - 40:
            grade.append('D')
        else:
            grade.append('F')
    return grade


student = int(input("Total number of students : "))
scores = input(f'Enter {student} score(s) :').split()
while len(scores)< student:
    scores = input(f'Enter {student} score(s) :').split()

scores = [int(num) for num in scores]
new_scores = scores[0:student]
best = max(new_scores)
grade = list()
cal_score()
for i in range(student):
    print(f'Student {i+1} score is {new_scores[i]} and grade is {grade[i]}')
