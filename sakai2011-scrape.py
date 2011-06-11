import lxml.html
from lxml import etree

sakai2011 = lxml.html.parse('http://www.concentra-cms.com/program/Sakai/2011-sakai-conference/')

rows = sakai2011.xpath("//div[@style='vertical-align:text-top;position:relative;margin-left:15px;margin-right:15px;']/table/tr")

monday = {}
tuesday = {}
wednesday = {}
thursday = {}

def do_session(cur_day, row):
  time = etree.tostring(row[0][0]).strip("<br/>").strip()
  starttime = time.split("-")[0].strip()
  if not cur_day.has_key(starttime):
    cur_day[starttime] = []
  cur_day[starttime].append(row)

def serialize_session(data):
  time = etree.tostring(data[0][0]).strip("<br/>").strip()
  room = etree.tostring(data[0][1]).strip("<br/>").strip()
  
  info = etree.tostring(data[1])
  info = info.replace('<td width="35%" class="body">','<p>')
  info = info.replace('</td>','</p>')
  info = info.replace("window.open('/program","window.open('http://www.concentra-cms.com/program")
  print("%s<br/>%s<br/>" % (time,room))
  print(info)
  
  #print("%s<br/>%s<br/>" % (time,room))
  #print("%s<br/>%s<br/>" % (data[1].text,etree.tostring(data[1][2])))
  #print(data[1][2].text)
  #if len(data[1]) > 3:
  #  print(etree.tostring(data[1][3]))
  

def mycmp(one, two):
  onehour = int(one.split(":")[0])
  onemin = int(one.split(":")[1].split(" ")[0])
  twohour = int(two.split(":")[0])
  twomin = int(two.split(":")[1].split(" ")[0])
  #print("%s, %s, %s, %s" % (onehour, onemin, twohour, twomin))
  if onehour > twohour:
    return 1
  elif onehour < twohour:
    return -1
  elif onemin > twomin:
    return 1
  elif onemin < twomin:
    return -1
  else:
    return 0

def serialize_day(dayname, data):
  print("<h1>%s</h1>" % (dayname))
  print("<table>")
  for key in sorted(data.iterkeys(), cmp=mycmp):
    if "AM" in key:
      print("<tr>")
      for row in data[key]:
        print("<td>")
        serialize_session(row)
        print("</td>")
      print("</tr>")
  for key in sorted(data.iterkeys(), cmp=mycmp):
    if "PM" in key:
      print("<tr>")
      for row in data[key]:
        print("<td>")
        serialize_session(row)
        print("</td>")
      print("</tr>")
  print("</table>")

def serialize_out():
  print("""<html><head>
<style type="text/css">
body {
  font-family: arial, sans-serif;
}
table {
  border-collapse:collapse;
}
td { 
  vertical-align: top;
}
table, td {
  border: 1px solid black;
}
</style>
</head><body>""")
  serialize_day("Monday", monday)
  serialize_day("Tuesday", tuesday)
  serialize_day("Wednesday", wednesday)
  serialize_day("Thursday", thursday)
  print("</body></html>")

for row in rows:
  cur_text = etree.tostring(row)
  if "Monday, June 13" in cur_text:
    cur_day = monday
  elif "Tuesday, June 14" in cur_text:
    cur_day = tuesday
  elif "Wednesday, June 15" in cur_text:
    cur_day = wednesday
  elif "Thursday, June 16" in cur_text:
    cur_day = thursday
  else:
    do_session(cur_day, row)
  
serialize_out()
