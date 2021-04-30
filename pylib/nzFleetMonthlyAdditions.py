import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

filePath = Path(__file__)
yearMonth = "202103"
baseName = "additions-to-the-national-vehicle-fleet"
ext = '.csv'
baseFileName = Path(Path(__file__).parent.parent, "data",
                    yearMonth, baseName)

tableName = 'table6'
fileName = baseFileName / (tableName+ext)
table6 = pd.read_csv(fileName,
                     header=0)
print(fileName)
print(table6)
# Get columns using regular expressions
# print(table6.filter(regex=r"(?i)mar"))
print(table6.filter(regex=r"(?i){:}".format("mar")))
#table3.dropna(axis=1, inplace=True)


def pickSubCols(df, colName):
    subCols = df.filter(regex=r"(?i){:}".format(colName))
    # Get First row as a dictionary
    firstRow = dict(subCols.loc[0])
    # swap key, values in firstRow
    # colNames = dict((v, k) for k, v in firstRow.items())
    #subCols = subCols[1:].rename(columns=colNames)
    subCols = subCols[1:].rename(columns=firstRow)
    return subCols


def top10Cars(df, month, pmonth):
    """
    df: Table contains month as first row and vehicle make, 
        count of vehicles as second row 
    """
    currentMonth = pickSubCols(df, month)
    pastMonth = pickSubCols(df, pmonth)
    htmlList = []
    print("make, ccount, count changep, position change")
    cpos = 1
    for cmake, ccount in zip(currentMonth['Vehicle make'], currentMonth['Count of vehicles']):
        ccount = int(ccount)
        if cmake in pastMonth['Vehicle make'].values:
            row = pastMonth.loc[pastMonth['Vehicle make'] == cmake]
            ppos = row.iloc[0].name
            pcount = int(row['Count of vehicles'])
            print(cmake, ccount, "{:} ({:.1f}%)".format(ccount-pcount, (ccount-pcount)/pcount*100),
                  ppos-cpos)
            htmlList.append([cmake, ccount,
                             "{:} ({:.1f}%)".format(ccount-pcount,
                                                    (ccount-pcount)/pcount*100),
                             ppos-cpos])
        else:
            print(cmake, ccount)
            htmlList.append([cmake, ccount, '-', '-'])
        cpos += 1

    return currentMonth, pastMonth, htmlList


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def bsTableBody(htmlList):
    thead = """
    <thead class="thead-inverse text-center">
    <tr>
    <th>Make</th>
    <th class="text-center">Count</th>
    <th class="text-center">Count Change</th>
    <th class="text-center">Position Change</th>
    </tr>
    </thead>
    """
    tbody = """
    <tbody>
    """
    for row in htmlList:
        make, count, countDiff, posDiff = row
        make = '<th class="text-primary">{:}</th>'.format(make)
        count = '<td>{:}</td>'.format(count)
        countDiff = '<td>{:}</td>'.format(countDiff)
        if is_number(posDiff):
            icon = '<i class="fa fa-arrow-up fa-lg text-success"/>'if int(
                posDiff) >= 0 else '<i class="fa fa-arrow-down fa-lg text-danger"/>'
        else:
            icon = ""
        posDiff = '<td> {:}  {:}</td>'.format(
            icon,
            posDiff)

        tr = """
        <tr >
        {:}
        {:}
        {:}
        {:}
        </tr>
        """.format(make,
                   count, countDiff, posDiff)
        tbody += tr
    tbody = "\n".join([tbody,
                       "</tbody>"])
    table = """
    <table class="table text-center table-bordered">
    """
    table = "\n".join([table,
                       thead,
                       tbody,
                       "</table>"])
    return table


c, p, table6HtmlList = top10Cars(table6, 'mar', 'feb')
print(bsTableBody(table6HtmlList))
# print(table1)
#table1.to_csv("../data/"+yearmonth+"/"+basename+"-table1.csv", index=False)
# table2.to_csv("../data/"+yearmonth+"/table2.csv", index=False)
# table3.to_csv("../data/"+yearmonth+"/table3.csv", index=False)

# table1.to_html("../data/"+yearmonth+"/table1.html", index=False)
#fig1, ax1 = plt.subplots()
# ax1.pie(table1["num"], labels=table1["vehicleType"],
#        autopct='%1.1f%%', shadow=True)
# ax1.legend()
# ax1.axis('equal')
# plt.show()
