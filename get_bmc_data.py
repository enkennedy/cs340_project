import sys
import pandas as pd

class Course:
    def __init__(self, id, prof, dept, level):
        self.id = id
        self.prof = prof
        self.dept = dept
        self.level = level

def getData(csv, constraints, prefs):

    #Read in csv data and assign integer ids
    data = pd.read_csv(csv)

    courses = {}
    depts = {}
    profs = {}
    times = []
    students = {}
    rooms = {}

    currStudent = 1
    currCourse = 1
    currDept = 1
    currProf = 1
    currRoom = 1
    
    for index, row in data.iterrows():

        course = int(row["Course ID"])
        if course not in courses:
            dept = str(row["Subject"])
            if dept not in depts:
                depts[dept] = currDept
                currDept += 1
            level = str(row["Catalog"])[1]
            prof = str(row["Instructor ID"])
            if prof not in profs:
                profs[prof] = currProf
                currProf += 1
            c = Course(currCourse, profs[prof], depts[dept], level)
            courses[course] = c
            currCourse += 1

        student = int(row["Student ID"])
        if student not in students:
            students[student] = [currStudent]
            currStudent += 1
        students[student].append(courses[course].id)
        
        room = str(row["Facil ID 1"])
        if room not in rooms:
            rooms[room] = [currRoom, 0]
            currRoom += 1
        rooms[room][1] += 1

        t = str(row["Start_1"])
        t2 = t.split(":")
        if "AM" in t:
            sTime = 60 * int(t2[0]) + int(t2[1][0:2])
        else:
            sTime = 60 * (int(t2[0]) + 12) + int(t2[1][0:2])
        t = str(row["End 1"])
        t2 = t.split(":")
        if "AM" in t:
            eTime = 60 * int(t2[0]) + int(t2[1][0:2])
        else:
            eTime = 60 * (int(t2[0]) + 12) + int(t2[1][0:2])
        time = [sTime, eTime]
        if time not in times:
            times.append(time)

    #Write data to constraints
    fileC = open(constraints, "w")
    fileC.write("Class Times\t" + str(len(times)) + "\n")
    for slot in times:
        fileC.write(str(slot[0]) + "\t" + str(slot[1]) + "\n")
    fileC.write("Rooms\t" + str(len(rooms)) + "\n")
    for r in rooms.values():
        fileC.write(str(r[0]) + "\t" + str(r[1]) + "\n")
    fileC.write("Classes\t" + str(len(courses)) + "\n")
    fileC.write("Teachers\t" + str(len(profs)) + "\n")
    for c in courses.values():
        fileC.write(str(c.id) + "\t" + str(c.dept) + "\t" + str(c.level) + "\t" + str(c.prof) + "\n")
    fileC.close()

    #Write data to prefs
    fileP = open(prefs, "w")
    fileP.write("Students\t" + str(len(students)) + "\n")
    for s in students.values():
        fileP.write(str(s[0]) + "\t")
        for cls in s[1:]:
            fileP.write(str(cls) + " ")
        fileP.write("\n")
    fileP.close()


if len(sys.argv) != 4:
  print ("Usage: " + sys.argv[0] + " <enrollment.csv> <student_prefs.txt> <constraints.txt>")
  exit(1)

getData(sys.argv[1], sys.argv[2], sys.argv[3])