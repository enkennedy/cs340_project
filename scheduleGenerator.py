import sys

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

class Slot:
  def __init__(self, time, room):
    self.time = time
    self.room = room

class ScheduledClass:
  def __init__(self, id, time, room, capacity, prof):
    self.id = id
    self.time = time
    self.room = room
    self.capacity = capacity
    self.prof = prof
    self.numEnrolled = 0
    self.students = []

def createSchedule(constraints, studentprefs, schedule):
  fileC = open(constraints, "r")
  fileP = open(studentprefs, "r")
  s = 0
  c = 0
  r = 0
  t = 0
  p = 0
  rooms = []
  slots = []
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
        professors[j].classes.append(int(cinfo[0]))
    line = fileC.readline()
  fileC.close()

  #Get preference info
  line = fileP.readline
  l = line.split()
  s = int(l[1])
  studentPreferences = [s][4]
  for i in range(0,s):
    line = fileP.readline()
    l = line.split()
    for j in range(1,5):
      studentPreferences[i][j-1] = int(l[j])
      classPopularity[int(l[j])-1].pop += 1
  fileP.close()

  roomsSorted = rooms.sorted(key = lambda x: x.capacity)
  classPopularity.sort(reverse = True, key = lambda x: x.pop)

  for room in roomsSorted:
    for i in reversed(range(0,t)):
      slots.append(Slot(room,i+1))

  #Create the schedule
    schedule = [c]
    for cls in classPopularity:
      slot = slots.pop()
      if slot.time in professors[cls.prof-1].times:
        temp = slot
        slot = slots.pop()
        slots.append(temp)
      scheduledCls = ScheduledClass(cls.id, slot.time, slot.room, rooms[slot.room-1].capacity, cls.prof)
      professors[cls.prof-1].times.append(slot.time)
      schedule[cls.id-1] = scheduledCls

  #Enroll students
  prefVal = 0
  for row in range(0,s):
    for i in range(0,3):
      currCls = schedule[studentPreferences[row][i]-1]
      if currCls.numEnrolled < currCls.capacity:
        conflict = False
        for j in range(0,i):
          prevCls = schedule[studentPreferences[row][j]-1]
          if prevCls.time == currCls.time:
            conflict = True
        if ~conflict:
          currCls.students.append(row+1)
          prefVal += 1

  #Output preference value and fit
  print(f"Student Preference Value: {prefVal}")
  print(f"Best Case Student Preference Value: {s * 4}")
  print(f"Fit Percentage: {prefVal / (s * 4)}%")

  #Write to output
  fileS = open(schedule, "w")
  fileS.write("Course Room Teacher Time Students\n")
  for cls in schedule:
    fileS.write(cls.id + " " + cls.room + " " + cls.prof + " " + cls.time)
    for student in cls.students:
      fileS.write(" " + student)
    fileS.write("\n")
  fileS.close()

def main():
  constraints = sys.argv[1]
  studentprefs = sys.argv[2]
  schedule = sys.argv[3]
  createSchedule(constraints, studentprefs, schedule)

if __name__ == "__main__":
  main()