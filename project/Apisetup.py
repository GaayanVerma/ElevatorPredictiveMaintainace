from fastapi import FastAPI
import datetime
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
from fastapi.responses import FileResponse
import pandas as pd
from modelpyth import model_variablereturn

data = pd.read_excel('E:/Minor Project/project/Final Data.xlsx')
dfinput=data[['ball-bearing','vibration','Distance']]

clf=model_variablereturn()

def convertstr_time(strdate):
    year, month, day = map(int, strdate.split('-'))
    redate = datetime.datetime(year, month, day)
    return redate


def predictvalueparcing(predict_days, ttinitial):
    ballb = []
    distii = []
    time = []
    labels = [0, 5, 10, 15, 20, 25, 30]
    for j in range(predict_days * 10):
        ballb.append(dfinput['ball-bearing'][ttinitial + j])
        distii.append(dfinput['Distance'][ttinitial + j])
        time.append(j)
    return ballb, distii, time


def predicted_duration(origindate, dateinitial, datefinal):
    oridate = convertstr_time(origindate)
    inidate = convertstr_time(dateinitial)
    findate = convertstr_time(datefinal)

    predict_days = (findate - inidate).days
    ttinitial = (inidate - oridate).days

    ball, diss, time = predictvalueparcing(predict_days, ttinitial)

    return ball, diss, time


def plotdistbargraph(origindate, dateinitial, datefinal):

    oridate=convertstr_time(origindate)
    findate=convertstr_time(datefinal)
    daysfrmori=(findate-oridate).days
    tempdiss=dfinput['Distance']
    distvalue=[]
    temp=0
    for i in range(7):
        for j in range(10):
            temp=temp+tempdiss[daysfrmori]
            daysfrmori=daysfrmori-1
        distvalue.append(temp)
        temp=0
    disdf={ 'Distance': [distvalue[0],distvalue[1],distvalue[2],distvalue[3],distvalue[4],distvalue[5],distvalue[6]],
            'Day': ['Monday', 'Tuesday', 'Wednesday','Thurday','Friday','Saturday','Sunday']
          }
    fig = px.bar(disdf, x='Day', y='Distance')
    pio.write_image(fig, 'E:\Minor Project\project\image\Bargraph.png')


def graphplotting(origindate, dateinitial, datefinal):
    ball, diss, time = predicted_duration(origindate, dateinitial, datefinal)
    inidate = convertstr_time(dateinitial)
    findate = convertstr_time(datefinal)
    oridate = convertstr_time(origindate)
    ttdays = (findate - inidate).days
    ttinitial = (inidate - oridate).days
    datte = []
    ballbb = []
    for i in range(ttdays * 10):
        datte.append(inidate)
        ballbb.append(dfinput['ball-bearing'][ttinitial])
        ttinitial = ttinitial + 1
        inidate = inidate + datetime.timedelta(hours=2, minutes=24)
    graphdf = {'Condition': ballbb,
               'Time': datte
               }
    fig = px.line(graphdf, x='Time', y='Condition')
    pio.write_image(fig, 'E:\Minor Project\project\image\Ballbearing.png')


def oppredmodel(origindate, dateinitial, datefinal):
    oridate = convertstr_time(origindate)
    inidate = convertstr_time(dateinitial)
    findate = convertstr_time(datefinal)
    datapoint=((findate-oridate).days)*10
    vi=dfinput['vibration'][datapoint]
    ballb=dfinput['ball-bearing'][datapoint]
    predicted=int(clf.predict([[ballb,vi]])[0])
    if predicted == 0:
        return "GOOD!"
    elif predicted == 1:
        return "Average!"
    elif predicted == 2:
        return "ALERT! ATTENTION REQURIED"

#originaldate: str, initialdate: str,finaldate: str graphplot/{originaldate}/{initialdate}/{finaldate}
app=FastAPI()
@app.get('/graphplot/{originaldate}')
def graphii(originaldate: str, initialdate: str,finaldate: str):
    graphplotting(originaldate, initialdate, finaldate)
    return FileResponse("E:\Minor Project\project\image\Ballbearing.png")

@app.get('/barchartplot/{originaldate}')
def barchartii(originaldate: str, initialdate: str,finaldate: str):
    plotdistbargraph(originaldate, initialdate, finaldate)
    return FileResponse("E:\Minor Project\project\image\Bargraph.png")

@app.get('/model/{originaldate}')
def predmodel(originaldate: str, initialdate: str,finaldate: str):
    return oppredmodel(originaldate, initialdate, finaldate)