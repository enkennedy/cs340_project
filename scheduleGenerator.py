import sys
import time

class RoomInfo:
  def __init__(self, id, capacity):
    self.id = id
    self.capacity = capacity

class ClassInfo:
  def __init__(self, id, prof):
    self.id = id
    self.prof = prof
    self.pop = 0

class ProfessorInfo:
  def __init__(self, id):
    self.id = id
    self.classes = []
    self.times = []

class ScheduledClass:
  def __init__(self, id, time, room, capacity, prof):
    self.id = id
    self.time = time
    self.room = room
    self.capacity = capacity
    self.prof = prof
    self.numEnrolled = 0
    self.students = []

def createSchedule(constraints, studentprefs, finalschedule):
  start = time.perf_counter()

  fileC = open(constraints, "r")
  fileP = open(studentprefs, "r")
  s = 0
  c = 0
  r = 0
  t = 0
  p = 0
  rooms = []
  classPopularity = []
  professors = []
  line = fileC.readline()

  #Get constraint info
  while line:
    l = line.split()
    if l[0] == "Class" and l[1] == "Times":
      t = int(l[2])
    if l[0] == "Rooms":
      r = int(l[1])
      for i in range(0,r):
        line = fileC.readline()
        rinfo = line.split()
        room = RoomInfo(int(rinfo[0]), int(rinfo[1]))
        rooms.append(room)
    if l[0] == "Classes":
      c = int(l[1])
    if l[0] == "Teachers":
      p = int(l[1])
      for i in range(0,p):
        prof = ProfessorInfo(i + 1)
        professors.append(prof)
      for j in range(0,c):
        line = fileC.readline()
        cinfo = line.split()
        cls = ClassInfo(int(cinfo[0]), int(cinfo[1]))
        classPopularity.append(cls)
        professors[int(cinfo[1])-1].classes.append(int(cinfo[0]))
    line = fileC.readline()
  fileC.close()

  #Get preference info
  line = fileP.readline()
  l = line.split()
  s = int(l[1])
  studentPreferences = [[None] * 4 for _ in range(s)]
  for i in range(0,s):
    line = fileP.readline()
    l = line.split()
    for j in range(1,5):
      studentPreferences[i][j-1] = int(l[j])
      classPopularity[int(l[j])-1].pop += 1
  fileP.close()

  roomsSorted = sorted(rooms, key = lambda x: x.capacity, reverse = True)
  classPopularity.sort(reverse = True, key = lambda x: x.pop)

  schedule = [None] * c
  currT = 1
  currR = 0
  len = c
  for i in range(0,c):
    room = roomsSorted[currR]
    cls = classPopularity[-1]
    professor = professors[cls.prof-1]
    idx = -1
    while currT in professor.times and idx > -len:
      idx -= 1
      temp = classPopularity[idx]
      professor = professors[temp.prof-1]
    if currT not in professor.times:
        cls = classPopularity.pop(idx)
        len -= 1
        scheduledCls = ScheduledClass(cls.id, currT, room.id, room.capacity, cls.prof)
        schedule[cls.id-1] = scheduledCls
        professor.times.append(currT)
    currT += 1
    if currT > t:
      currT = 0
      currR += 1

  end = time.perf_counter()
  elapsedtime = end - start
  print(f"Runtime: {elapsedtime}")

  #Enroll students
  prefVal = 0
  studentBusy = [set() for _ in range(s)]
  for row in range(0,s):
    for i in range(0,4):
      currCls = schedule[studentPreferences[row][i]-1]
      if currCls is not None and currCls.numEnrolled < currCls.capacity and currCls.time not in studentBusy[row]:
        currCls.students.append(row+1)
        currCls.numEnrolled += 1
        studentBusy[row].add(currCls.time)
        prefVal += 1

  #Output preference value and fit
  print(f"Student Preference Value: {prefVal}")
  print(f"Best Case Student Preference Value: {s * 4}")
  print(f"Fit Ratio: {prefVal / (s * 4)}")

  #Write to output
  fileS = open(finalschedule, "w")
  fileS.write("Course\tRoom\tTeacher\tTime\tStudents\n")
  for cls in schedule:
    if cls is None:
      continue
    fileS.write(str(cls.id) + "\t" + str(cls.room) + "\t" + str(cls.prof) + "\t" + str(cls.time) + "\t")
    for student in cls.students:
      fileS.write(str(student) + " ")
    fileS.write("\n")
  fileS.close()

def main():
  constraints = str(sys.argv[1])
  studentprefs = str(sys.argv[2])
  schedule = str(sys.argv[3])
  createSchedule(constraints, studentprefs, schedule)

if __name__ == "__main__":
  main()