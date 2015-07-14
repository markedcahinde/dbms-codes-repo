import sys
import csv
import operator

def csv_reader(filename):
  with open(filename, mode='r') as csvfile:
    fileDialect = csv.Sniffer().sniff(csvfile.read(1024))
    csvfile.seek(0)

    reader = csv.DictReader(csvfile, dialect=fileDialect)
    mydict = {}

    for row in reader:
      for k, v in row.iteritems():
        mydict.setdefault(k, []).append(v) 

    return mydict

#1. Which Region have the most State Universities?
def get_region_with_most_suc():
  f = open('suc_ph.csv')
  suc = {}
  for index, line in enumerate(f):
    row = line.split(',')
    if row[0] in suc:
      suc[row[0]] += 1
    else:
      suc[row[0]] = 1
  f.close()
  print suc
  suc_list = sorted(suc.items(), key = operator.itemgetter(1), reverse = True)
  print suc_list
  print "1. The region with the most SUC is " + suc_list[0][0]

#2. Which Region have the most enrollees?
def get_region_with_most_enrollees_by_school_year(school_year):
  mydict = csv_reader('suc_ph.csv')  

  for k, v in mydict.items():
    for i in range(0, len(v)):
      if v[i].isdigit():
        v[i] = int(v[i])
      else:
        if v[i] == '-' or v[i] == ' -   ':
          v[i] = 0
    if k.find(school_year) != -1 and k.find('enrolment'):
      sorted_list = sorted(mydict[k], reverse = True)
      for v in mydict[k]:
        if sorted_list[0] == v:
          index = mydict[k].index(v)
          
  print "2. The region with the most SUC enrollees is " + mydict['region'][index]

#3. Which Region have the most graduates?
def get_region_with_most_graduates_by_school_year(school_year):
  mydict = csv_reader('suc_ph.csv') 

  for k, v in mydict.items():
    for i in range(0, len(v)):
      if v[i].isdigit():
        v[i] = int(v[i])
      else:
        if v[i] == '-' or v[i] == ' -   ':
          v[i] = 0
    if k.find(school_year) != -1 and k.find('gradutes'):
      sorted_list = sorted(mydict[k], reverse = True)
      for v in mydict[k]:
        if sorted_list[0] == v:
          index = mydict[k].index(v)
    
  print "3. The region with the most SUC graduates is " + mydict['region'][index]

#4 top 3 SUC who has the chepeast tuition fee by schoolyear
def get_top_3_cheapest_by_school_year(level, school_year):
  mydict = csv_reader('tuitionfeeperunitsucproglevel20102013.csv') 

  tuition_list = []
  for k, v in mydict.items():
    if k.find(school_year) != -1 and k.find(level.lower()) != -1:
      for i in range(0, len(v)):
        if v[i].isdigit():
          v[i] = int(v[i])
          tuition_list.append(v[i])
          tuition_list = sorted(tuition_list)
  print "4. Top 3 cheapest SUC for BS level in school year 2010-2011"
  for n in range(0,3):
    for k, v in mydict.items():
      if k.find(school_year) != -1 and k.find(level.lower()) != -1:
        for i in v:
          if tuition_list[n] == i:
            print "\t", n+1, ". ", mydict['suc'][v.index(i)]


#5 top 3 SUC who has the most expensive tuition fee by schoolyear
def get_top_3_most_expensive_by_school_year(level, school_year):
  mydict = csv_reader('tuitionfeeperunitsucproglevel20102013.csv') 

  tuition_list = []
  for k, v in mydict.items():
    if k.find(school_year) != -1 and k.find(level.lower()) != -1:
      for i in range(0, len(v)):
        if v[i].isdigit():
          v[i] = int(v[i])
          tuition_list.append(v[i])
          tuition_list = sorted(tuition_list, reverse = True)
  print "5. Top 3 expensive SUC for BS level in school year 2010-2011"
  for n in range(0,3):
    for k, v in mydict.items():
      if k.find(school_year) != -1 and k.find(level.lower()) != -1:
        for i in v:
          if tuition_list[n] == i:
            print "\t", n+1, ". ", mydict['suc'][v.index(i)]


#6 list all SUC who have increased their tuition fee from school year 2010-2011 to 2012-2013
def all_suc_who_have_increased_tuition_fee():
  f = open('tuitionfeeperunitsucproglevel20102013.csv')
  suc_bs = []
  suc_ms = []
  suc_phd = []
  index = 2
  for i, l in enumerate(f):
    row = l.split(',')
    if row[2].isdigit() and row[5].isdigit() and row[8].isdigit():
      if row[2] != row[5] != row[8]:
        suc_bs.append(row[1])
    if row[3].isdigit() and row[6].isdigit() and row[9].isdigit():
      if row[3] != row[6] != row[9]:
        suc_ms.append(row[1])
    if row[4].isdigit() and row[7].isdigit() and row[10].isdigit():
      if row[4] != row[7] != row[10]:
        suc_phd.append(row[1])
  print "6. List of SUC who have increased their tuition fee from school year 2010-2011 to 2012-2013"
  # print "   Technological University of the Philippines, Apayao State College, Marikina Polytechnic College, Surigao State College of Technolgoy"
  print "  LEVEL: BS ", suc_bs
  print "  LEVEL: MS ", suc_ms
  print "  LEVEL: PHD ", suc_phd

#7 which discipline has the highest passing rate?
def get_discipline_with_highest_passing_rate_by_shool_year(year):
  f = open('performancesucprclicensureexam20102012.csv')
  index = []
  dict = {}
  for i, l in enumerate(f):
    row = l.split(',')
    [index.append(j) for j, k in enumerate(row) if k.find(year) != -1]
    if len(index) > 1:
      for x, y in enumerate(index):
        if x == 0:
          if row[y].isdigit() and row[index[x+1]].isdigit():
            dict[i] = [row[1], row[2], int((float(row[y])/float(row[index[x+1]]))*100)]
  sorted_list = sorted(dict.values(), key = operator.itemgetter(2), reverse = True)
  discipline = []

  count = 0
  for v in dict.values():
    if v[1] == 'Accountancy':
      count += 1

  for v in range(0, len(sorted_list)):
    if sorted_list[0][2] == sorted_list[v][2] and sorted_list[v][1] not in discipline:
      discipline.append(sorted_list[v][1])

  print "7. The discipline which has the highest passing rate is ", sorted(discipline)
  
#8 list top 3 SUC with the most passing rate by discipline by school year
def get_top_3_suc_performer_by_discipline_by_year(discipline, school_year):
  f = open('performancesucprclicensureexam20102012.csv')
  index = []
  dict = {}
  for i, l in enumerate(f):
    row = l.split(',')
    [index.append(j) for j, k in enumerate(row) if k.find(school_year) != -1]
    if len(index) > 1:
      for x, y in enumerate(index):
        if x == 0:
          if row[y].isdigit() and row[index[x+1]].isdigit():
            dict[i] = [row[1], row[2], int((float(row[y])/float(row[index[x+1]]))*100)]
  sorted_list = sorted(dict.values(), key = operator.itemgetter(2), reverse = True)

  print "8. Top 3  SUC with highest passing rate in Accountancy for school year 2010-2011"
  count = 0
  for v in sorted_list:
    if v[1] == discipline and count != 3:
      print " ", count+1, ". ", v[0]
      count += 1

def main():
  get_region_with_most_suc()
  get_region_with_most_enrollees_by_school_year('2010-2011')
  get_region_with_most_graduates_by_school_year('2010-2011')
  get_top_3_cheapest_by_school_year('BS', '2010-2011')
  get_top_3_most_expensive_by_school_year('BS', '2010-2011')
  all_suc_who_have_increased_tuition_fee()
  get_discipline_with_highest_passing_rate_by_shool_year('2010')
  get_top_3_suc_performer_by_discipline_by_year('Accountancy', '2011')


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
