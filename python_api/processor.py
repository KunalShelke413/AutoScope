from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from storage import get_data
import json
import pandas as pd
import numpy as np
import re
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# last_file = "../backend/uploads/data.csv"
# ext = os.path.splitext(last_file)[1]

character_columns, time_columns, location_terms, Numerical_columns, Contact, SUM_COLUMNS, COUNT_COLUMNS= get_data()

# if ext==".csv":
#    df=pd.read_csv(last_file,encoding='unicode_escape')
# elif ext==".xlsx" or ext==".xls":
#    df=pd.read_excel(last_file)
# elif ext==".json":
#    df=pd.read_json(last_file)

csv=["Breast_cancer_data.csv","Canada.csv","categories.csv","Chocolate Sales.csv","Diwali Sales Data.csv","employees.csv","full_order_details.csv","Most Runs - 2022.csv","order_details.csv","Practicle 7 tableau_project_dataset (1).csv","products.csv","remain.csv","sales_data_sample.csv","Sales_Data_Big.csv","Sample - Superstore.csv","student_performance_dataset.csv","superstore_sales.csv","suppliers.csv","test_sheet.csv","try.csv","x_y_axis_terms.csv","Sales_without_NaNs.csv"]
i=6
df=pd.read_csv(csv[i],encoding='unicode_escape')
print(csv[i])

total_column_count=0
total_row_count=0
column_name=[]
null_columns=[]
droped_column=[]
numerical_columns=[]
phone_number_column=[]
alpha_columns=[]
date_columns=[]
location_columns=[]
country=[]
city=[]
state=[]
postal_code=[]
area=[]
address=[]
coordinates=[]
new_cols=[]
shape=[]
org_shape=df.shape
summary=["org_shape","shape","total_column_count","total_row_count","column_name",
         "null_columns","droped_column","numerical_columns","alpha_columns",
         "date_columns","location_columns","phone_number_column","new_cols"]

shape=list(df.shape)
df.columns = df.columns.str.strip().str.replace(r'\s+', '_', regex=True).str.lower()
df.drop_duplicates(inplace=True)
column_name=df.columns
null_columns=df.columns[df.isnull().any()].tolist()

droped_column=[]
for i in null_columns:
  if (df[i].count()<= (len(df)//3)):
    droped_column.append(i)
    df.drop(columns=[i],inplace=True)
total_column_count=len(df.columns)
total_row_count=len(df)

numerical_columns=df.select_dtypes(include="number").columns.tolist()
alpha_columns=df.select_dtypes(include=['object','string']).columns.tolist()
date_columns=df.select_dtypes(include=['datetime']).columns.tolist()

#check date in numerical
from os import replace
for check_date in numerical_columns:
  check=check_date.translate(str.maketrans("_-/","   ")).split()
  for i in check[:]:
    for j in time_columns:
      if i==j:
        if check_date not in date_columns:
          date_columns.append(check_date)
        if check_date not in time_columns:
          time_columns.append(check_date)
          break
        else:
          break
for r in date_columns:
  if r in numerical_columns:
    numerical_columns.remove(r)

#check aplha column to dataset
for j in alpha_columns:
  for i in character_columns:
    if j==i:
      flag=0
      break
    flag=1
  if flag==1:
    character_columns.append(j)

#check date column from dataset
for i in alpha_columns:
  for j in time_columns:
    if i==j:
      if i not in date_columns:
        date_columns.append(i)
      break
for r in date_columns:
  if r in alpha_columns:
    alpha_columns.remove(r)

#check numerical column from dataset
for i in alpha_columns:
  for j in Numerical_columns:
    if i==j:
      if i not in numerical_columns:
        try:
          df[i]=df[i].astype(str).str.replace(r"[,%$]", "", regex=True).str.strip()
          df[i]=pd.to_numeric(df[i],errors='ignore')
        finally:
          numerical_columns.append(i)
      break
for r in numerical_columns:
  if r in alpha_columns:
    alpha_columns.remove(r)

#numerical detector___________check later
for i in alpha_columns:
    for j in Numerical_columns:
        pattern = (
            r'(^' + re.escape(j) + r'$|' +
            r'^' + re.escape(j) + r'([_\-\s]|$)|' +
            r'([_\-\s]|^)' + re.escape(j) + r'$|' +
            r'.*'+re.escape(j)+r'.*'
            r')'
        )
        if re.search(pattern, i, re.IGNORECASE):
            if i not in numerical_columns:
              v=df.loc[0,i]
              val="1234567890%.$-*+"
              nflag=0
              for fst in v:
                if fst in val:
                  nflag=nflag+1
              if nflag==(len(v)):
                df[i]=(df[i]
                  .astype(str)
                  .str.replace(r"[,_\-%\$\*]", "", regex=True)
                  .str.strip()
                  )
                df[i]=pd.to_numeric(df[i],errors="coerce")
                numerical_columns.append(i)
              break

for r in numerical_columns:
    if r in alpha_columns:
        alpha_columns.remove(r)

#date time detector
for i in alpha_columns:
    for j in time_columns:
        pattern = (
            r'(^' + re.escape(j) + r'$|' +
            r'^' + re.escape(j) + r'([_\-\s]|$)|' +
            r'([_\-\s]|^)' + re.escape(j) + r'$|' +
            r'.*' + re.escape(j) + r'.*'
            r')'
        )
        if re.search(pattern, i, re.IGNORECASE):
            if i not in date_columns:
                date_columns.append(i)
            break

def detect_and_convert_date(col,fmt,check):
    col = col.astype(str).str.strip()
    if col.str.fullmatch(r"\d{1,2}").all():
        return col.astype(int), None, None
    if col.str.fullmatch(r"\d{2,4}").all():
        return col.astype(int), None, None
    if check[0:4].isdigit():
        fmt="%Y-%m-%d"
    if len(check)>10:
        fmt="%m-%d-%Y %H:%M:%S.%f"
    parsed = pd.to_datetime(col, errors="coerce", format=fmt)
    if parsed.isnull().all():
        fmt="%m-%d-%Y"
        parsed = pd.to_datetime(col, errors="coerce")
    month_col = parsed.dt.month
    year_col = parsed.dt.year
    return parsed.dt.strftime(fmt), month_col,year_col
for r in date_columns:
    df[r]=df[r].replace("/","-")
    fmt="%d-%m-%Y"
    check = df.loc[0,r]
    check = str(check).strip()
    try:
        if (check[3] in ['-','/'] and check[4].isalpha()) or (check[3].lower().isalpha()):
            flag=2
            df[r]=df[r].astype(str).str.lower().str.strip()
            df[r]=df[r].replace({"jan":"01","feb":"02","mar":"03","apr":"04","may":"05","jun":"06",
                             "jul":"07","aug":"08","sep":"09","oct":"10","nov":"11","dec":"12","january":"01",
                             "february":"02","march":"03","april":"04","june":"06",
                             "july":"07","august":"08","september":"09","october":"10",
                             "november":"11","december":"12"},
                            regex=True)
            df[r] = pd.to_datetime(df[r],errors="coerce",format="%d-%m-%y").dt.strftime("%d-%m-%y")
            if len(df.loc[0,r])==8:
                fmt="%d-%m-%y"
    except IndexError:
        fmt="%d-%m-%Y"
    finally:
        df[r], month,year = detect_and_convert_date(df[r],fmt,check)
        if month is not None:
            df[r + "_month"] = month
            new_cols.append(r + "_month")

        if year is not None:
            df[r + "_year"] = year
            new_cols.append(r + "_year")

        if r in alpha_columns:
            alpha_columns.remove(r)
for new in new_cols:
    date_columns.append(new)

# filter duplicate date columns
r=[]
for i in new_cols:
    for j in date_columns:
        count=len(df)-1
        check=0
        for k in range(0,len(df)-1):
            if df.loc[k,i]==df.loc[k,j] and i!=j:
                check=check+1
            else:
                break
        if count==check:
            r.append(i)

for i in r:
    date_columns.remove(i)
    df.drop(columns=[i],inplace=True)

column_name=df.columns

#Location detector
for i in location_terms:
  for j in range(len(location_terms[i])):
    for k in alpha_columns:
      if k==location_terms[i][j]:
        if k not in location_columns:
          location_columns.append(k)
          if i=="country":
            country.append(k)
          elif i=="city":
            city.append(k)
          elif i=="state":
            state.append(k)
          elif i=="area":
            area.append(k)
          elif i=="postal":
            postal_code.append(k)
          elif i=="address":
            address.append(k)
          elif i=="coordinates":
            coordinates.append(k)
    for n in numerical_columns:
      if n==location_terms[i][j]:
        if n not in location_columns:
          location_columns.append(n)
          if i=="postal":
            postal_code.append(n)
for r in location_columns:
  if r in alpha_columns:
    alpha_columns.remove(r)
for rn in location_columns:
  if rn in numerical_columns:
    numerical_columns.remove(rn)

#non alphabetical pushed to numerical
for i in alpha_columns:
  flag=0
  add=0
  sub=0
  nct=0
  fstvl=0
  lstvl=0
  special=0
  value=df.loc[0,i]
  val="1234567890"
  alpha = "abcdefghijklmnopqrstuvwxyz"
  Alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  if (len(value)==1) and ((value in alpha) or (value in Alpha)):
    continue
    if isinstance(value, str):
      val="1234567890"
      vald="1234567890."
      value=value.replace(",","").strip()
      for tr in range(len(value)):
        if (value[tr] not in val) and (value[tr]==value[0]):
          fstvl=1
        elif (value[tr] not in val) and (value[tr]==value[-1]):
          lstvl=1
        elif (value[tr] in val):
          flag=flag+1
        elif (value[tr]=="."):
          flag=flag+1
          special=special+1
    if (fstvl==1) and ((len(value)-1)==flag):
      for cv in range(len(df[i])):
        val_str = str(df.loc[cv, i])
        for see in val_str:
          if (sub==0) and (see=="-"):
            sub=1
          elif see not in vald:
            val_str = val_str.replace(see, "")
        df.loc[cv, i] = val_str
      df[i]=(df[i]
            .astype(str)
            .str.replace(",","",regex=False)
            .str.strip()
            )
      df[i]=pd.to_numeric(df[i],errors="coerce")
      numerical_columns.append(i)
    elif (lstvl==1) and ((len(value)-1)==flag):
      for cv in range(len(df[i])):
        val_str = str(df.loc[cv, i])
        for see in val_str:
          if (sub==0) and (see=="-"):
            sub=1
          elif see not in vald:
            val_str = val_str.replace(see, "")
        df.loc[cv, i] = val_str
      df[i]=(df[i]
            .astype(str)
            .str.replace(",","",regex=False)
            .str.strip()
            )
      df[i]=pd.to_numeric(df[i],errors="coerce")
      numerical_columns.append(i)
    elif (special==1) and ((len(value))==flag):
      for cv in range(len(df[i])):
        val_str = str(df.loc[cv, i])
        for see in val_str:
          if (sub==0) and (see=="-"):
            sub=1
          elif see not in vald:
            val_str = val_str.replace(see, "")
        df.loc[cv, i] = val_str
      df[i]=(df[i]
            .astype(str)
            .str.replace(",","",regex=False)
            .str.strip()
            )
      df[i]=pd.to_numeric(df[i],errors="coerce")
      numerical_columns.append(i)
    elif (special==0) and ((len(value))==flag) and (lstvl==0) and (fstvl==0):
      for cv in range(len(df[i])):
        val_str = str(df.loc[cv, i])
        for see in val_str:
          if (sub==0) and (see=="-"):
            sub=1
          elif see not in vald:
            val_str = val_str.replace(see, "")
        df.loc[cv, i] = val_str
      df[i]=(df[i]
            .astype(str)
            .str.replace(",","",regex=False)
            .str.strip()
            )
      df[i]=pd.to_numeric(df[i],errors="coerce")
      numerical_columns.append(i)
  else:
    value=str(value).strip()
    if value.isdigit():
      df[i]=df[i].astype(str).str.strip()
      df[i]=pd.to_numeric(df[i],errors="coerce")
      numerical_columns.append(i)
    elif (isinstance(value,str)):
      for cv in value:
        if cv in val:
          nct=nct+1
      if len(value)==nct:
        df[i]=(df[i]
            .astype(str)
            .str.replace(r"[,_\-%\$\*]", "", regex=True)
            .str.strip()
            )
        df[i]=pd.to_numeric(df[i],errors="coerce")
        numerical_columns.append(i)

for r in numerical_columns:
  if r in alpha_columns:
    alpha_columns.remove(r)

#non numerical pushed to alphabetical
for i in numerical_columns:
  flag=0
  add=0
  sub=0
  value = df.loc[0, i]
  if isinstance(value, str):
    val="1234567890"
    vald="1234567890."
    alpha="abcdefghijklmnopqrstuvwxyz"
    Alpha="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    value=value.replace(",","").strip()
    for tr in range(1,len(value)):
      if (isinstance(value[0],str) and (value[tr] in val) ) or ((value[0] in val) and (value[tr] in val)) or ((value[tr-1] in val) and (isinstance(value[-1],str))):
        flag=1
      elif (value[tr] == "."):
        flag=1
      else:
        add=add+1
  flag=flag+add
  if (flag==1) and (((value[0] not in alpha) and (value[0] not in Alpha)) and ((value[-1] not in alpha) and (value[-1] not in Alpha))):
    if len(df[i])<=100:
        check_len=len(df[i])
    else:
        check_len=60
    n=np.random.randint(1, len(df[i])//3)
    for cv in range(n,check_len):
      val_str = str(df.loc[cv, i])
      for see in val_str:
        if (sub==0) and (see=="-"):
          sub=1
        elif (see not in vald):
          val_str = val_str.replace(see, "")
      df.loc[cv, i] = val_str
    df[i] = (
    df[i]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.strip())
    df[i] = pd.to_numeric(df[i], errors="coerce")
  elif (flag>1) or ((flag==1) and (((value[0] in alpha) or (value[0] in Alpha)) or ((value[-1] in alpha) or (value[-1] in Alpha)))):
    alpha_columns.append(i)
for r in alpha_columns:
  if r in numerical_columns:
    numerical_columns.remove(r)

#phone number detector from numerical column
for i in numerical_columns:
  if i in Contact:
    phone_number_column.append(i)
    numerical_columns.remove(i)

#filter alpha columns
for r in alpha_columns:
  if r in numerical_columns:
    alpha_columns.remove(r)
  elif r in date_columns:
    alpha_columns.remove(r)
  elif r in location_columns:
    alpha_columns.remove(r)

#formatting alpha columns
for i in alpha_columns:
  df[i]=df[i].str.strip()
  df[i]=df[i].str.title()

df.drop_duplicates(inplace=True)
shape=list(df.shape)

for i in numerical_columns:
    unique_vals=set(df[i].dropna().unique())
    if unique_vals.issubset({1,0}):
        SUM_COLUMNS.append(i)

for col in alpha_columns:
    df[col] = df[col].astype(str).str.lower().str.strip()
    unique_vals = set(df[col].dropna().unique())
    if unique_vals.issubset({"yes", "no", "y", "n"}):
        df[col] = df[col].replace(
            {"yes": 1, "no": 0, "y": 1, "n": 0}
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")
        numerical_columns.append(col)
        SUM_COLUMNS.append(col)
    elif unique_vals.issubset({"true", "false"}):
        df[col] = df[col].replace(
            {"true": 1, "false": 0}
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")
        numerical_columns.append(col)
        SUM_COLUMNS.append(col)
    elif unique_vals.issubset({"m", "f"}):
        df[col] = df[col].replace(
            {"m": "Male", "f": "Female"}
        )
    if col not in numerical_columns:
        df[col] = df[col].str.title()
alpha_columns = [c for c in alpha_columns if c not in numerical_columns]

dct=0
lct=0
for i in alpha_columns:
    check=df.loc[0,i]
    for j in check:
        if j.isdigit():
           dct+=1
        elif j=="-":
            lct+=1
    if dct+lct==len(check):
        COUNT_COLUMNS.append(i)
    dct=0
    lct=0

for i in alpha_columns:
    df[i]=df[i].fillna("Unknown")
for i in numerical_columns:
    df[i]=df[i].fillna(df[i].median())
for i in location_columns:
    df[i]=df[i].fillna("Unknown")

df = df.replace([np.inf, -np.inf], 0)
df = df.where(pd.notnull(df), 0)

sidechart=0
chart1=0
chart2=0
p1=0
p2=0
p3=0
p4=0
X_Qualitative=[]
X_Quantitative=[]
X_Location=[]
X_Time=[]
single=[]
N_single=[]
P_single=[]
mix=[]
N_mix=[]
L_mix=[]
P_mix=[]
line_charts=[]
heat_maps=[]
histogram_charts=[]
scatter_plots=[]
box_plots=[]
area_charts=[]
bubble_charts=[]
dia=[mix,N_mix,P_single,single,N_mix,L_mix,P_single,line_charts,heat_maps,histogram_charts,scatter_plots,box_plots,area_charts,bubble_charts]
Dia_ID=[]
Access=[]
bar_check=[]
u4=[]
def check(i,a,bar_check,p):
    if Access[i][a] and (i!=6 and i!=2) and (p==0):
        p=dia[int(Access[i][a][0])][int(Access[i][a][1])][int(Access[i][a][2])][int(Access[i][a][3])]
        bar_check.append(Access[i][a])
        a+=1
    return a,bar_check,p
def B_check(i,bar_check,p):
    if Access[i][0] and (i!=6 and i!=2) and (p==0) and Access[i][0] not in bar_check:
        p=dia[int(Access[i][0][0])][int(Access[i][0][1])][int(Access[i][0][2])][int(Access[i][0][3])]
        bar_check.append(Access[i][0])
    return bar_check,p
def four(column,u4,a,b,c,d,A,B,C,D):
    for i in column:
        check=len(df[i].unique())
        if check>1 and check<5:
            new=df[i].value_counts()
            for i in len(new):
                if new.index[i] not in u4:
                    if a==0:
                        a=new.values[i]
                        u4.append(a)
                        A=new.index[i]
                    elif b==0:
                        b=new.values[i]
                        u4.append(b)
                        B=new.index[i]
                    elif c==0:
                        c=new.values[i]
                        u4.append(c)
                        C=new.index[i]
                    elif d==0:
                        d=new.values[i]
                        u4.append[d]
                        D=new.index[i]
    return u4,a,b,c,d,A,B,C,D

for i in column_name:
    a=len(df[i].unique())
    if a<=15 :
        if i in alpha_columns:
            X_Qualitative.append(i)
        elif i in numerical_columns:
            X_Quantitative.append(i)
        elif i in date_columns:
            X_Time.append(i)

column_name = df.columns
result = {col: [] for col in column_name}
pie_result = {col: [] for col in column_name}
line_result = {col: [] for col in column_name}
heat_result = {col: [] for col in column_name}
histogram_result = {col: [] for col in column_name}
scatter_result = {col: [] for col in column_name}
box_result = {col: [] for col in column_name}
area_result = {col: [] for col in column_name}
bubble_result = {col: [] for col in column_name}

# Bar charts>>>
j=0
k=0

for col_index, col_name in enumerate(X_Qualitative):
    unique_vals = df[col_name].unique()
    if len(unique_vals) < 3 or len(unique_vals)>15:
        single.append([])
        # grouped = df.groupby(col_name)[numerical_columns].sum()
        if numerical_columns in SUM_COLUMNS:
            grouped = df.groupby(col_name)[numerical_columns].sum()
        elif numerical_columns in COUNT_COLUMNS:
            grouped = df.groupby(col_name)[numerical_columns].count()
        else:
            grouped = df.groupby(col_name)[numerical_columns].sum()
        i=0
        for category in unique_vals:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=numerical_columns,
                y=grouped.loc[category],
                text=grouped.loc[category],
                hovertemplate=
                "<b>Column:</b> %{x}<br>" +
                "<b>Value:</b> %{y}<br>" +
                "<extra></extra>"
            ))
            fig.update_layout(
                title=f"{category} summary for column {col_name}",
                xaxis_title="Numerical Columns",
                yaxis_title="Sum",
                hoverlabel=dict(bgcolor="white"),
                margin=dict(t=30, b=10, l=10, r=10)
            )
            single[j].append([])
            single[j][i].append(fig)
            result[col_name].append(fig)
            i=i+1
        j=j+1
    else:
        mix.append([])
        si=0
        for num_col in numerical_columns:
            # grouped = df.groupby(col_name)[num_col].sum()
            if num_col in SUM_COLUMNS:
                grouped = df.groupby(col_name)[num_col].sum()
            elif num_col in COUNT_COLUMNS:
                grouped = df.groupby(col_name)[num_col].count()
            elif col_name in COUNT_COLUMNS:
                grouped = df.groupby(col_name)[num_col].count()
            else:
                grouped = df.groupby(col_name)[num_col].sum()
            fig = go.Figure()
            x_vals = list(grouped.index)
            y_vals = grouped.values.tolist()
            fig.add_trace(go.Bar(
                x=x_vals,
                y=y_vals,
                text=grouped.values,
                hovertemplate=
                "<b>Category:</b> %{x}<br>" +
                "<b>Value:</b> %{y}<br>" +
                "<extra></extra>"
            ))
            fig.update_layout(
                title=f"{num_col} by {col_name}",
                xaxis_title=col_name,
                yaxis_title=num_col,
                margin=dict(t=30, b=10, l=10, r=10)
            )
            mix[k].append([])
            mix[k][si].append(fig)
            result[col_name].append(fig)
            result[num_col].append(fig)
            si=si+1
        k=k+1

j=0
k=0

for col_index, col_name in enumerate(X_Quantitative):
    unique_vals = df[col_name].unique()
    if len(unique_vals) < 3:
        N_single.append([])
        # grouped = df.groupby(col_name)[numerical_columns].sum()
        if numerical_columns in SUM_COLUMNS:
            grouped = df.groupby(col_name)[numerical_columns].sum()
        elif numerical_columns in COUNT_COLUMNS:
            grouped = df.groupby(col_name)[numerical_columns].count()
        else:
            grouped = df.groupby(col_name)[numerical_columns].sum()
        i=0
        for category in unique_vals:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=numerical_columns,
                y=grouped.loc[category],
                text=grouped.loc[category],
                hovertemplate=
                "<b>Column:</b> %{x}<br>" +
                "<b>Value:</b> %{y}<br>" +
                "<extra></extra>"
            ))
            fig.update_layout(
                title=f"{category} summary for column {col_name}",
                xaxis_title="Numerical Columns",
                yaxis_title="Sum",
                hoverlabel=dict(bgcolor="white"),
                margin=dict(t=30, b=10, l=10, r=10)
            )
            N_single[j].append([])
            N_single[j][i].append(fig)
            result[col_name].append(fig)
            i=i+1
        j=j+1
    else:
        N_mix.append([])
        si=0
        for num_col in numerical_columns:
            # grouped = df.groupby(col_name)[num_col].sum()
            if num_col in SUM_COLUMNS:
                grouped = df.groupby(col_name)[num_col].sum()
            elif num_col in COUNT_COLUMNS:
                grouped = df.groupby(col_name)[num_col].count()
            elif col_name in COUNT_COLUMNS:
                grouped = df.groupby(col_name)[num_col].count()
            else:
                grouped = df.groupby(col_name)[num_col].sum()
            x_vals = list(grouped.index)
            y_vals = grouped.values.tolist()
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=x_vals,
                y=y_vals,
                text=grouped.values,
                hovertemplate=
                "<b>Category:</b> %{x}<br>" +
                "<b>Value:</b> %{y}<br>" +
                "<extra></extra>"
            ))
            fig.update_layout(
                title=f"{num_col} by {col_name}",
                xaxis_title=col_name,
                yaxis_title=num_col,
                margin=dict(t=30, b=10, l=10, r=10)
            )
            N_mix[k].append([])
            N_mix[k][si].append(fig)
            result[col_name].append(fig)
            result[num_col].append(fig)
            si=si+1
        k=k+1

j=0

for col_index, col_name in enumerate(location_columns):
    L_mix.append([])
    si=0
    for num_col in numerical_columns:
        
        # grouped = df.groupby(col_name)[num_col].sum()
        if num_col in SUM_COLUMNS:
            grouped = df.groupby(col_name)[num_col].sum()
        elif col_name in SUM_COLUMNS:
            grouped = df.groupby(col_name)[num_col].sum()
        elif num_col in COUNT_COLUMNS:
            grouped = df.groupby(col_name)[num_col].count()
        elif col_name in COUNT_COLUMNS:
            grouped = df.groupby(col_name)[num_col].count()
        else:
            grouped = df.groupby(col_name)[num_col].sum()
        x_vals = list(grouped.index)
        y_vals = grouped.values.tolist()
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=x_vals,
            y=y_vals,
            text=grouped.values,
            hovertemplate=
            "<b>Category:</b> %{x}<br>" +
            "<b>Value:</b> %{y}<br>" +
            "<extra></extra>"
        ))
        fig.update_layout(
            title=f"{num_col} by {col_name}",
            xaxis_title=col_name,
            yaxis_title=num_col,
            margin=dict(t=30, b=10, l=10, r=10)
        )
        L_mix[j].append([])
        L_mix[j][si].append(fig)
        result[col_name].append(fig)
        result[num_col].append(fig)
        si=si+1
    j=j+1

#Pie charts>>>
j=0

for i in column_name:
    si=0
    if len(df[i].unique()) <= 8 and len(df[i].unique())>1:
        P_single.append([])
        counts = df[i].value_counts()
        fig = go.Figure()
        # labels = counts.index
        labels = counts.index.astype("category").codes
        labels = labels.astype("int16")
        values = counts.values.astype("int")
        fig.add_trace(go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            hovertemplate="<b>%{label}</b><br>Count: %{value}<extra></extra>"
        ))
        fig.update_layout(
            title=f"Distribution of {i}",
            title_font=dict(size=13),
            # legend_title="Categories",
            margin=dict(t=30, b=10, l=10, r=10)
        )
        P_single[j].append([])
        P_single[j][si].append(fig)
        pie_result[i].append(fig)
        si=si+1
        j=j+1

j=0
for i in X_Qualitative:
    P_mix.append([])
    for l in numerical_columns:
        si=0
        grouped = df.groupby(i)[l].sum()
        fig = go.Figure()
        labels = grouped.index.astype("category").codes
        labels = labels.astype("int16")
        values = grouped.values.astype("int")
        fig.add_trace(go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            hovertemplate="<b>%{label}</b><br>Value: %{value}<extra></extra>"
        ))
        fig.update_layout(
           title=f"Distribution of {l} by {i}",
          #  legend_title=i,
           title_font=dict(size=13),
           margin=dict(t=30, b=10, l=10, r=10)
        )
        P_mix[j].append([])
        P_mix[j][si].append(fig)
        pie_result[i].append(fig)
        pie_result[l].append(fig)
        si=si+1
    j=j+1
# line chart

def line_chart(date_col, num_col, freq="ME"):
    temp = df[[date_col, num_col]].dropna()

    temp[date_col] = pd.to_datetime(
        temp[date_col],
        errors="coerce",
        dayfirst=True
    )

    temp = temp.dropna(subset=[date_col])

    temp = (
        temp
        .set_index(date_col)
        .resample(freq)[num_col]
        .mean()
        .reset_index()
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=temp[date_col],
        y=temp[num_col],
        mode="lines+markers"
    ))

    fig.update_layout(
        title=f"Line Chart: {num_col} over time",
        xaxis_title=date_col,
        yaxis_title=num_col,
        margin=dict(t=30, b=10, l=10, r=10)
    )

    return fig


i=0
j=0
for d in date_columns:
    line_charts.append([])
    for n in numerical_columns:
        fig = line_chart(d, n)
        line_charts[i].append([])
        line_charts[i][j].append(fig)
        line_result[d].append(fig)
        line_result[n].append(fig)
        j+=1
    i+=1
    j=0


#heat map

def heat_map(numerical_columns):
    corr = df[numerical_columns].corr()

    fig = go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale="Viridis"
        )
    )

    fig.update_layout(title="Correlation Heatmap",
                      margin=dict(t=30, b=10, l=10, r=10))
    return fig


heat_maps.append([])
fig = heat_map(numerical_columns)
if fig:
   heat_maps_check=1
heat_maps[0].append([fig])
for nl in numerical_columns:
    heat_result[nl].append(fig)


# histogram_charts

def histogram_chart(num_col):
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=df[num_col],
        nbinsx=30
    ))

    fig.update_layout(
        title=f"Histogram of {num_col}",
        xaxis_title=num_col,
        yaxis_title="Count",
        margin=dict(t=30, b=10, l=10, r=10)
    )
    return fig

i=0
histogram_charts.append([])
for n in numerical_columns:
    fig = histogram_chart(n)
    histogram_charts[0].append([])
    histogram_charts[0][i].append(fig)
    histogram_result[n].append(fig)
    i+=1


# scatter plot

def scatter_plot(x_col, y_col):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[y_col],
        mode="markers"
    ))

    fig.update_layout(
        title=f"Scatter Plot: {x_col} vs {y_col}",
        xaxis_title=x_col,
        yaxis_title=y_col,
        margin=dict(t=30, b=10, l=10, r=10)
    )
    return fig


k=0
l=0
for i in range(len(numerical_columns)):
    scatter_plots.append([])
    for j in range(i+1,len(numerical_columns)):
        d = numerical_columns[i]
        n = numerical_columns[j]
        fig = scatter_plot(d, n)
        scatter_plots[k].append([])
        scatter_plots[k][l].append(fig)
        scatter_result[d].append(fig)
        scatter_result[n].append(fig)
        l+=1
    k+=1
    l=0


# box plot

def box_plot(num_col):
    fig = go.Figure()
    fig.add_trace(go.Box(
        y=df[num_col],
        boxmean=True
    ))

    fig.update_layout(
        title=f"Box Plot of {num_col}",
        yaxis_title=num_col,
        margin=dict(t=30, b=10, l=10, r=10)
    )
    return fig


i=0
box_plots.append([])
for n in numerical_columns:
    fig = box_plot(n)
    box_plots[0].append([])
    box_plots[0][i].append(fig)
    box_result[n].append(fig)
    i+=1

# area_plots

def area_chart(date_col, num_col):
    temp = df[[date_col, num_col]].dropna()

    temp[date_col] = pd.to_datetime(
        temp[date_col],
        errors="coerce",
        dayfirst=True
    )

    temp = temp.dropna(subset=[date_col])

    temp = (
        temp
        .set_index(date_col)
        .resample("ME")[num_col]
        .sum()
        .reset_index()
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=temp[date_col],
        y=temp[num_col],
        fill="tozeroy",
        mode="lines"
    ))

    fig.update_layout(
        title=f"Area Chart: {num_col}",
        xaxis_title=date_col,
        yaxis_title=num_col,
        margin=dict(t=30, b=10, l=10, r=10)
    )
    return fig


i=0
j=0
for d in date_columns:
    area_charts.append([])
    for n in numerical_columns:
        fig = area_chart(d, n)
        area_charts[i].append([])
        area_charts[i][j].append(fig)
        area_result[d].append(fig)
        area_result[n].append(fig)
        j+=1
    i+=1
    j=0


#bubble_chart

def bubble_chart(x_col, y_col, size_col):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[y_col],
        mode="markers",
        marker=dict(
            size=df[size_col],
            sizemode="area",
            sizeref=2.*max(df[size_col])/(40.**2),
            showscale=True
        )
    ))

    fig.update_layout(
        title="Bubble Chart",
        xaxis_title=x_col,
        yaxis_title=y_col,
        margin=dict(t=30, b=10, l=10, r=10)
    )
    return fig


l=0
m=0
for i in range(len(numerical_columns)):
    bubble_charts.append([])
    for j in range(i + 1, len(numerical_columns)):
        for k in range(j + 1, len(numerical_columns)):
            x = numerical_columns[i]
            y = numerical_columns[j]
            size = numerical_columns[k]
            fig=bubble_chart(x, y, size)
            bubble_charts[l].append([])
            bubble_charts[l][m].append(fig)
            bubble_result[x].append(fig)
            m+=1
    l+=1
    m=0

# <-------------------------------------------------comming soon------------------------------------------------>

# def tree_map(df, path_cols, value_col):
#     fig = px.treemap(
#         df,
#         path=path_cols,
#         values=value_col
#     )

#     fig.update_layout(title="Tree Map")
#     return fig

# fig = tree_map(
#     df,
#     path_cols=["country", "state", "city"],
#     value_col="amount_collected"
# )

# fig.show()

# fig = tree_map(
#     df,
#     path_cols=["department"],
#     value_col="total_sales"
# )

# fig.show()

# fig = tree_map(
#     df,
#     path_cols=["campaign", "agent_name"],
#     value_col="total_calls"
# )

# fig.show()

# <-------------------------------------------------comming soon------------------------------------------------>

result = {
    k: list({id(fig): fig for fig in v}.values())
    for k, v in result.items()
}
pie_result = {
    k: list({id(fig): fig for fig in v}.values())
    for k, v in pie_result.items()
}
line_result = {
    k: list({id(fig): fig for fig in v}.values())
    for k, v in line_result.items()
}
heat_result = {
    k: list({id(fig): fig for fig in v}.values())
    for k, v in heat_result.items()
}
histogram_result = {
    k: list({id(fig): fig for fig in v}.values())
    for k, v in histogram_result.items()
}
scatter_result = {
    k: list({id(fig): fig for fig in v}.values())
    for k, v in scatter_result.items()
}
box_result = {
    k: list({id(fig): fig for fig in v}.values())
    for k, v in box_result.items()
}
area_result = {
    k: list({id(fig): fig for fig in v}.values())
    for k, v in area_result.items()
}
bubble_result = {
    k: list({id(fig): fig for fig in v}.values())
    for k, v in bubble_result.items()
}

filtered_result = {k: v for k, v in result.items() if v}
filtered_pie_result = {k: v for k, v in pie_result.items() if v}
filtered_line_result = {k: v for k, v in line_result.items() if v}
filtered_heat_result = {k: v for k, v in heat_result.items() if v}
filtered_histogram_result = {k: v for k, v in histogram_result.items() if v}
filtered_scatter_result = {k: v for k, v in scatter_result.items() if v}
filtered_box_result = {k: v for k, v in box_result.items() if v}
filtered_area_result = {k: v for k, v in area_result.items() if v}
filtered_bubble_result = {k: v for k, v in bubble_result.items() if v}

i=-1
for all in dia:
    i+=1
    for j in range(0,len(all)):
        for k in range(len(all[j])):
            for l in range(len(all[j][k])):
                Dia_ID.append(str(i)+str(j)+str(k)+str(l))

for i in range(len(dia)):
    Access.append([])
    for val in (Dia_ID):
        if val[0]==str(i):
            Access[i].append(val)

count=0
for all in dia:
    for i in range(0,len(all)):
        for j in range(len(all[i])):
            for k in range(len(all[i][j])):
                count+=1
print("Total graphs displayed:",count)

pc=2
for i in range(len(Access[pc])):
    if i ==0:                   
        p1=dia[int(Access[pc][i][0])][int(Access[pc][i][1])][int(Access[pc][i][2])][int(Access[pc][i][3])]
        bar_check.append(Access[pc][i]) 
    elif i==1:
        p2=dia[int(Access[pc][i][0])][int(Access[pc][i][1])][int(Access[pc][i][2])][int(Access[pc][i][3])]
        bar_check.append(Access[pc][i])
    elif i==2:
        p3=dia[int(Access[pc][i][0])][int(Access[pc][i][1])][int(Access[pc][i][2])][int(Access[pc][i][3])]
        bar_check.append(Access[pc][i])
    elif i==3:
        p4=dia[int(Access[pc][i][0])][int(Access[pc][i][1])][int(Access[pc][i][2])][int(Access[pc][i][3])]
        bar_check.append(Access[pc][i])
if p1==0 or p2==0 or p3==0 or p4==0:
    pc=6
    if Access[pc]:
        if p1!=0:
            if p2!=0:
                if p3!=0:
                    if p4!=0:
                        pass
                    else:
                        p4=dia[int(Access[pc][0][0])][int(Access[pc][0][1])][int(Access[pc][0][2])][int(Access[pc][0][3])]
                        bar_check.append(Access[pc][0])
                else:  
                    for i in range(len(Access[pc])):
                        if i ==0:
                            p3=dia[int(Access[pc][i][0])][int(Access[pc][i][1])][int(Access[pc][i][2])][int(Access[pc][i][3])]
                            bar_check.append(Access[pc][i])
                        elif i==1:
                            p4=dia[int(Access[pc][i][0])][int(Access[pc][i][1])][int(Access[pc][i][2])][int(Access[pc][i][3])]
                            bar_check.append(Access[pc][i])  
            else:
                for i in range(len(Access[pc])):
                    if i ==0:
                        p2=dia[int(Access[pc][i][0])][int(Access[pc][i][1])][int(Access[pc][i][2])][int(Access[pc][i][3])]
                        bar_check.append(Access[pc][i])
                    elif i==1:
                        p3=dia[int(Access[pc][i][0])][int(Access[pc][i][1])][int(Access[pc][i][2])][int(Access[pc][i][3])]
                        bar_check.append(Access[pc][i])
                    elif i==2:
                        p4=dia[int(Access[pc][i][0])][int(Access[pc][i][1])][int(Access[pc][i][2])][int(Access[pc][i][3])]
                        bar_check.append(Access[pc][i])                
        else:
            for i in range(len(Access[pc])):
                if i ==0:
                    p1=dia[int(Access[pc][i][0])][int(Access[pc][i][1])][int(Access[pc][i][2])][int(Access[pc][i][3])]
                    bar_check.append(Access[pc][i])
                elif i==1:
                    p2=dia[int(Access[pc][i][0])][int(Access[pc][i][1])][int(Access[pc][i][2])][int(Access[pc][i][3])]
                    bar_check.append(Access[pc][i])
                elif i==2:
                    p3=dia[int(Access[pc][i][0])][int(Access[pc][i][1])][int(Access[pc][i][2])][int(Access[pc][i][3])]
                    bar_check.append(Access[pc][i])
                elif i==3:
                    p4=dia[int(Access[pc][i][0])][int(Access[pc][i][1])][int(Access[pc][i][2])][int(Access[pc][i][3])]
                    bar_check.append(Access[pc][i])

a=0
for i in range(len(Access)):
    try:
        a,bar_check,p1=check(i,a,bar_check,p1)
        a,bar_check,p2=check(i,a,bar_check,p2)
        a,bar_check,p3=check(i,a,bar_check,p3)
        a,bar_check,p4=check(i,a,bar_check,p4)
        if p1!=0 and p2!=0 and p3!=0 and p4!=0:
            break
        else:
            a=0
    except IndexError:
        continue

for i in range(len(Access)):
    try:
        bar_check,sidechart=B_check(i,bar_check,sidechart)
        bar_check,chart1=B_check(i,bar_check,chart1)
        bar_check,chart2=B_check(i,bar_check,chart2)
        if chart1!=0 and chart2!=0 and sidechart!=0 :
            break
    except IndexError:
        continue
if sidechart==0 or chart1==0 or chart2==0:
    for i in Dia_ID:
        if i not in bar_check and i not in Access[2] and i not in Access[6]:
            if sidechart==0:
                sidechart=dia[int(i[0])][int(i[1])][int(i[2])][int(i[3])]
            elif chart1==0:
                chart1=dia[int(i[0])][int(i[1])][int(i[2])][int(i[3])]
            elif chart2==0:
                chart2=dia[int(i[0])][int(i[1])][int(i[2])][int(i[3])]

if heat_maps_check==1:
   chart2=chart1
   chart1=sidechart
   sidechart=dia[8][0][0][0]

a, b, c, d, A, B, C, D = 0, 0, 0, 0, 0, 0, 0, 0

try:
    for i in numerical_columns:
        if df[i].sum() not in u4 and a==0:
            a=df[i].sum()
            u4.append(a)
            A="Total "+i
        elif df[i].sum() not in u4 and b==0:
            b=df[i].sum()
            u4.append(b)
            B="Total "+i
        elif df[i].sum() not in u4 and c==0:
            c=df[i].sum()
            u4.append(c)
            C="Total "+i
        elif df[i].sum() not in u4:
            d=df[i].sum()
            u4.append(d)
            D="Total "+i
except:
    try:
        u4,a,b,c,d,A,B,C,D=four(alpha_columns,u4,a,b,c,d,A,B,C,D)
    except:
        u4,a,b,c,d,A,B,C,D=four(location_columns,u4,a,b,c,d,A,B,C,D)


@app.get("/p1plot")
def p1_plot():
    fig_json = json.loads(json.dumps(p1, cls=PlotlyJSONEncoder))   # <--- KEY STEP
    return JSONResponse(content=fig_json)
@app.get("/p2plot")
def p1_plot():
    fig_json = json.loads(json.dumps(p2, cls=PlotlyJSONEncoder))   # <--- KEY STEP
    return JSONResponse(content=fig_json)
@app.get("/p3plot")
def p3_plot():
    fig_json = json.loads(json.dumps(p3, cls=PlotlyJSONEncoder))   # <--- KEY STEP
    return JSONResponse(content=fig_json)
@app.get("/p4plot")
def p4_plot():
    fig_json = json.loads(json.dumps(p4, cls=PlotlyJSONEncoder))   # <--- KEY STEP
    return JSONResponse(content=fig_json)
if heat_maps_check==1:
    @app.get("/sideplot")
    def side_plot():
        fig_json = json.loads(json.dumps(sidechart, cls=PlotlyJSONEncoder))   # <--- KEY STEP
        return JSONResponse(content=fig_json)
else:
    @app.get("/sideplot")
    def side_plot():
        fig_json = json.loads(json.dumps(sidechart, cls=PlotlyJSONEncoder))   # <--- KEY STEP
        return JSONResponse(content=fig_json)
@app.get("/chart1plot")
def chart1_plot():
    fig_json = json.loads(json.dumps(chart1, cls=PlotlyJSONEncoder))   # <--- KEY STEP
    return JSONResponse(content=fig_json)
@app.get("/chart2plot")
def chart2_plot():
    fig_json = json.loads(json.dumps(chart2, cls=PlotlyJSONEncoder))   # <--- KEY STEP
    return JSONResponse(content=fig_json)
@app.get("/alpdes")
def get_alpdes():
    obj_cols = df.select_dtypes(include="object")
    if obj_cols.empty:
        return {"Categorical Data": ["Not Found"]}
    alpdes = df.describe(include="object")
    alpdes = alpdes.replace([np.inf, -np.inf], None)
    alpdes = alpdes.where(alpdes.notna(), None)
    return alpdes.to_dict()
@app.get("/numdes")
def get_numdes():
    numdes = df.describe()
    numdes = numdes.replace([np.inf, -np.inf], None)
    numdes = numdes.where(numdes.notna(), None)
    return numdes.to_dict()
@app.get("/allcol")
def get_cols():
    return {"columns": list(column_name)}

@app.get("/process_filtered_result")
def process_data_filtered_result():
    response = {}

    for col, figs in filtered_result.items():
        if figs:
            response[col] = [
                json.loads(json.dumps(fig, cls=PlotlyJSONEncoder))
                for fig in figs
            ]

    return JSONResponse(content=response)

@app.get("/process_filtered_pie_result")
def process_data_filtered_pie_result():
    response = {}

    for col, figs in filtered_pie_result.items():
        if figs:
            response[col] = [
                json.loads(json.dumps(fig, cls=PlotlyJSONEncoder))
                for fig in figs
            ]

    return JSONResponse(content=response)


@app.get("/process_filtered_line_result")
def process_data_filtered_line_result():
    response = {}

    for col, figs in filtered_line_result.items():
        if figs:
            response[col] = [
                json.loads(json.dumps(fig, cls=PlotlyJSONEncoder))
                for fig in figs
            ]

    return JSONResponse(content=response)

@app.get("/process_filtered_histogram_result")
def process_data_filtered_histogram_result():
    response = {}

    for col, figs in filtered_histogram_result.items():
        if figs:
            response[col] = [
                json.loads(json.dumps(fig, cls=PlotlyJSONEncoder))
                for fig in figs
            ]

    return JSONResponse(content=response)

@app.get("/process_filtered_scatter_result")
def process_data_filtered_scatter_result():
    response = {}

    for col, figs in filtered_scatter_result.items():
        if figs:
            response[col] = [
                json.loads(json.dumps(fig, cls=PlotlyJSONEncoder))
                for fig in figs
            ]

    return JSONResponse(content=response)

@app.get("/process_filtered_box_result")
def process_data_filtered_box_result():
    response = {}

    for col, figs in filtered_box_result.items():
        if figs:
            response[col] = [
                json.loads(json.dumps(fig, cls=PlotlyJSONEncoder))
                for fig in figs
            ]

    return JSONResponse(content=response)

@app.get("/process_filtered_area_result")
def process_data_filtered_area_result():
    response = {}

    for col, figs in filtered_area_result.items():
        if figs:
            response[col] = [
                json.loads(json.dumps(fig, cls=PlotlyJSONEncoder))
                for fig in figs
            ]

    return JSONResponse(content=response)

@app.get("/process_filtered_bubble_result")
def process_data_filtered_bubble_result():
    response = {}

    for col, figs in filtered_bubble_result.items():
        if figs:
            response[col] = [
                json.loads(json.dumps(fig, cls=PlotlyJSONEncoder))
                for fig in figs
            ]

    return JSONResponse(content=response)

@app.get("/process")
def process_data():
    
    return {
    "onename":str(A),
    "one":int(a),
    "twoname": str(B),
    "two": int(b),
    "threename": str(C),
    "three":int(c) ,
    "fourname":str(D),
    "four": int(d),
    "summary": "go",
    }