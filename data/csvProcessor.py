import csv
import pandas as pd
from scipy.spatial.distance import cdist


def readFromCSV(Dateiname):
    df = pd.read_csv(Dateiname, delimiter=";")
    df.Y = df.Y.str.replace('.', '')
    df.X = df.X.str.replace('.', '')
    df.Y = df.Y.str.replace(',', '.')
    df.X = df.X.str.replace(',', '.')
    df['signature'] = "(" + df['Y'] + " " + df['X'] + ")"
    df.PLZ = df.PLZ.astype(str)
    df.Strasse = df.Strasse.astype(str)
    df['streetandplz'] = "(" + df['PLZ'] + " " + df['Strasse'] + ")"
    df.Y = df.Y.astype(float)
    df.X = df.X.astype(float)
    df.Y = df.Y.astype(int)
    df.X = df.X.astype(int)
    return df


def createDayCSV(df, name):
    df = df.drop_duplicates(subset=['streetandplz'])
    # Bei CSV muss zuerst erste Spalte und erste Zeile gelöscht werden um eingelesen werden zu können
    ergebnis = pd.DataFrame(cdist(df[['X', "Y"]], df[['X', "Y"]]), index=df["streetandplz"], columns=df["streetandplz"])
    ergebnis.to_csv(name + ".csv", sep=";", decimal=".")


def bedarfeErmitteln(df, weekday):
    Bedarfe = {}
    for i in range(len(df)):
        if df.iloc[i]["streetandplz"] not in Bedarfe.keys():
            Bedarfe[df.iloc[i]["streetandplz"]] = df.iloc[i]["Menge"]
        else:
            Bedarfe[df.iloc[i]["streetandplz"]] = Bedarfe[df.iloc[i]["streetandplz"]] + df.iloc[i]["Menge"]

    with open(weekday + 'bedarfe.csv', 'w', newline="") as csv_file:
        writer = csv.writer(csv_file)
        for key, value in Bedarfe.items():
            writer.writerow([key, value])


df = readFromCSV("Menge1.csv")

df['Datum'] = pd.to_datetime(df['Datum'], dayfirst=True)
df['day_of_week'] = df['Datum'].dt.day_name()
df["day_of_week"] = df["day_of_week"].astype(str)
weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
dfs = [df[(df['day_of_week'] == day) | (df.Datum.isnull())] for day in weekday]

for i in range(len(weekday)):
    bedarfeErmitteln(dfs[i], weekday[i])
    createDayCSV(dfs[i], weekday[i])
