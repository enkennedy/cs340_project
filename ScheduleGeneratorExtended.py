import sys
import time

class RoomInfo:
  def __init__(self, id, capacity):
    self.id = id
    self.capacity = capacity

class TimeInfo:
  def __init__(self, start, end):
    self.start = start
    self.end = end
    self.overlap = []

class ClassInfo:
  def __init__(self, id, dept, level, prof):
    self.id = id
    self.dept = dept
    self.level = level
    self.prof = prof
    #self.pop = 0

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
  times = []
  classPopularity = []
  professors = []
  line = fileC.readline()

  #Get constraint info
  while line:
    l = line.split()
    if l[0] == "Class" and l[1] == "Times":
      t = int(l[2])
      for i in range(0,t):
        line = fileC.readline()
        tinfo = line.split()
        times.append(TimeInfo(int(tinfo[0]),int(tinfo[1])))
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
        cls = ClassInfo(int(cinfo[0]), int(cinfo[1]), int(cinfo[2]), int(cinfo[3]))
        classPopularity.append(cls)
        professors[int(cinfo[1])-1].classes.append(int(cinfo[0]))
    line = fileC.readline()
  fileC.close()

  #Get preference info
  optPrefVal = 0
  line = fileP.readline()
  l = line.split()
  s = int(l[1])
  studentPreferences = []
  for i in range(0,s):
    line = fileP.readline()
    l = line.split()
    studentPreferences.append(l[1:])
    optPrefVal += len(l) - 1
  fileP.close()

  times.sort(key = lambda x: x.start) #times sorted by start time
  for i in range(0,t):
    for j in range(0,t):
      if (times[j].end >= times[i].start and times[j].end <= times[i].end) or (times[j].start <= times[i].end and times[j].start >= times[i].start) or (times[j].start <= times[i].start and times[j].end >= times[i].end):
        times[i].overlap.append(times[j])

  roomsSorted = sorted(rooms, key = lambda x: x.capacity, reverse = True)
  classPopularity.sort(key = lambda x: x.level)
  classPopularity.sort(key = lambda x: x.dept)

  schedule = [None] * c
  currT = 0
  currR = 0
  length = c
  for i in range(0,c):
    room = roomsSorted[currR]
    slot = times[currT]
    cls = classPopularity[-1]
    professor = professors[cls.prof-1]
    idx = -1
    while slot in professor.times and idx > -length:
      idx -= 1
      temp = classPopularity[idx]
      professor = professors[temp.prof-1]
    if slot not in professor.times:
        cls = classPopularity.pop(idx)
        length -= 1
        scheduledCls = ScheduledClass(cls.id, slot, room.id, room.capacity, cls.prof)
        schedule[cls.id-1] = scheduledCls
        professor.times.append(slot)
        professor.times.extend(slot.overlap)
    currT += 1
    if currT >= t:
      currT = 0
      currR += 1
    if currR >= r:
      break

  end = time.perf_counter()
  elapsedtime = end - start
  print(f"Runtime: {elapsedtime}")

  #Enroll students
  prefVal = 0
  studentBusy = [[] for _ in range(s)]
  for i in range(0,s):
    for j in studentPreferences[i]:
        cls = schedule[int(j)-1]
        if cls is not None and cls.numEnrolled < cls.capacity and cls.time not in studentBusy[i]:
            cls.students.append(i+1)
            cls.numEnrolled += 1
            studentBusy[i].append(cls.time)
            studentBusy[i].extend(cls.time.overlap)
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
    startHour = cls.time.start // 60
    startMin = cls.time.start % 60
    endHour = cls.time.end // 60
    endMin = cls.time.end % 60
    #fileS.write(str(cls.id) + "\t" + str(cls.room) + "\t" + str(cls.prof) + "\t" + str(cls.time.start) + "-" + str(cls.time.end) + "\t")
    fileS.write(str(cls.id) + "\t" + str(cls.room) + "\t" + str(cls.prof) + "\t" + str(startHour) + ":" + str(startMin) + "-" + str(endHour) + ":" + str(endMin) + "\t")
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