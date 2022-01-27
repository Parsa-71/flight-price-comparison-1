#Parsa Fallah-adl
import requests
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
url="https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US/USD/en-US/SEA-sky/HND-sky/2021-01"
headers = {
 'x-rapidapi-key': "1edac6a2e6msh0e090afc0e7ff36p13c924jsn9313a18fc4ac",
 'x-rapidapi-host':
"skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
 }
response = requests.request("GET", url, headers=headers)
SEA_HND_jan = response.text.split('}, {\n')
SEA_HND_jan_count = {0 : {"direct" : 0, "indirect" : 0},
 1 : {"direct" : 0, "indirect" : 0},
 2 : {"direct" : 0, "indirect" : 0},
 3 : {"direct" : 0, "indirect" : 0},
 4 : {"direct" : 0, "indirect" : 0},
 5 : {"direct" : 0, "indirect" : 0},
 6 : {"direct" : 0, "indirect" : 0}}
SEA_HND_jan_ave_price = {0 : {"direct" : 0, "indirect" : 0},
 1 : {"direct" : 0, "indirect" : 0},
 2 : {"direct" : 0, "indirect" : 0},
 3 : {"direct" : 0, "indirect" : 0},
 4 : {"direct" : 0, "indirect" : 0},
 5 : {"direct" : 0, "indirect" : 0},
 6 : {"direct" : 0, "indirect" : 0}}
for quote in SEA_HND_jan:
 x = re.findall('"MinPrice" : ([0-9]+),', quote)
 y = re.findall('"Direct" : ([ft].+),', quote)
 z = re.findall('"DepartureDate" : "([0-9]{4}-[0-9]{2}-[0-9]{2})',
quote)
for a in x:
 price = a
 for b in y:
  if b == "true":
    flight = "direct"
  elif b == "false":
    flight = "indirect"
 for c in z:
  day = pd.Timestamp(c)
 dpt_day = day.dayofweek
 SEA_HND_jan_count[dpt_day][flight] += 1
 SEA_HND_jan_ave_price[dpt_day][flight] += (int(price) /
SEA_HND_jan_count[dpt_day][flight])
def dayOfWeek(d):
 if d == 0:
  day = "Monday"
 elif d == 1:
  day = "Tuesday"
 elif d == 2:
  day = "Wednesday"
 elif d == 3:
  day = "Thursday"
 elif d == 4:
  day = "Friday"
 elif d == 5:
  day = "Saturday"
 else:
  day = "Sunday"
 return day
SEA_HND_direct = list()
SEA_HND_indirect = list()
for day in SEA_HND_jan_ave_price:
 print("Day of week: ", dayOfWeek(day))
 flights = SEA_HND_jan_ave_price[day]
 direct = round(flights["direct"], 2)
 SEA_HND_direct.append(direct)
 indirect = round(flights["indirect"], 2)
 SEA_HND_indirect.append(indirect)
 if direct == 0:
  direct =("N/A")
 print("Direct flight average price: $", direct)
 print("Indirect flight average price: $", indirect)
 print()
barWidth = 0.25
bars1 = SEA_HND_direct
bars2 = SEA_HND_indirect
r1 = np.arange(len(bars1))
r2 = [x + barWidth for x in r1]
plt.style.use('seaborn')
plt.bar(r1, bars1, width=barWidth, label='direct')
plt.bar(r2, bars2, width=barWidth, label='indirect')
plt.xticks([r + barWidth for r in range(len(bars1))], ["Monday",
"Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
plt.xlabel('Day of the Week')
plt.ylabel('USD ($)')
plt.title('SEA -> Tokyo, Japan January 2021')
plt.legend()
plt.show()
