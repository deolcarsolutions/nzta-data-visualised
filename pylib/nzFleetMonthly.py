import pandas as pd
import matplotlib.pyplot as plt

yearmonth = "202103"
basename = "../data/New-Zealand-Vehicle-Fleet-Status"
filename = basename+"-"+yearmonth+"-sanitised.xls"
ef = pd.ExcelFile(filename)
print(ef.sheet_names)

contents = ef.parse('Contents')
table1 = ef.parse('Table 1')
table2 = ef.parse('Table 2')
table3 = ef.parse('Table 3')

table1.dropna(axis=1, inplace=True)
#table2.dropna(axis=1, inplace=True)
#table3.dropna(axis=1, inplace=True)

print(table1)
table1.to_csv("../data/"+yearmonth+"/table1.csv", index=False)
table2.to_csv("../data/"+yearmonth+"/table2.csv", index=False)
table3.to_csv("../data/"+yearmonth+"/table3.csv", index=False)

table1.to_html("../data/"+yearmonth+"/table1.html", index=False)
#fig1, ax1 = plt.subplots()
#ax1.pie(table1["num"], labels=table1["vehicleType"],
#        autopct='%1.1f%%', shadow=True)
#ax1.legend()
#ax1.axis('equal')
#plt.show()
