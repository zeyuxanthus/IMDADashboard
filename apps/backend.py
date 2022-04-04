import pandas as pd

modules = ['Python', 'DWH', 'Java', 'Linux', 'Hadoop', 'Apache Hive', 'Spark']

url = 'https://raw.githubusercontent.com/zeyuxanthus/IMDADashboard/master/datasets/report_card.csv'

df = pd.read_csv(url)

def region(df1):
    count = df1.shape[0]

    title = df1['Title'][0]
    completed  = df1['Completed Module'][0]
    total = df1['Total Module'][0]

    return count, title, completed, total

def getCount(df):
    count, title, completed, total = region(df)
    
    return count, title, completed, total

def getDF(region):
    global df

    r = ''
    if region == 'Singapore':
        r = 'SG'
    return df[df['Region'] == f'{r}']

def getStudent(df):
    return df['Name'].tolist()

def getStudentInfo(df, name):
    return df[df['Name'] == name]

def scores(df):
    string = ''
    for i in modules:
        result = df[i].tolist()
        result = result[0]
        if result > 0:
            string = string+i+': '+str(result)+'  '

    return string

def project(df):
    string = ''
    projects = df['Projects'].tolist()
    if pd.notna(projects):
        projects = projects[0].split(',')
        string = 'Projects involved: '
        for i in range(len(projects)):
            if(i < len(projects)-1):
                string = string + projects[i] + ', '
            else:
                string = string + projects[i]
    else:
        string = 'Not involved in any project in the moment.'

    return string