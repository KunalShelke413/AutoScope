from fastapi import FastAPI
import pandas as pd
import pandas as pd
import numpy as np
import re
import random
from os import replace
import plotly.graph_objects as go

character_columns=['name', 'department', 'departments', 'team', 'teams', 'product', 'products',
 'region', 'regions', 'subject', 'subjects', 'class', 'school', 'schools',
 'assignment', 'assignments', 'age group', 'age groups', 'disease', 'diseases',
 'hospital', 'hospitals', 'city', 'cities', 'campaign', 'campaigns',
 'platform', 'platforms', 'segment', 'segments', 'ad type', 'ad types',
 'device', 'devices', 'app version', 'app versions', 'feature', 'features',
 'day', 'days', 'error type', 'error types', 'country', 'countries', 'state', 'states',
 'zone', 'zones', 'income bracket', 'income brackets', 'gender', 'genders',
 'warehouse', 'warehouses', 'category', 'categories', 'supplier', 'suppliers',
 'delivery route', 'delivery routes', 'shipment date', 'shipment dates',
 'storage section', 'storage sections', 'developer', 'developers',
 'module', 'modules', 'sprint', 'sprints', 'bug type', 'bug types',
 'task', 'tasks', 'product type', 'product types', 'payment method',
 'payment methods', 'customer', 'coupon', 'coupon codes', 'store branch',
 'store branches', 'content type', 'content types', 'influencer',
 'influencers', 'hashtag', 'hashtags', 'posting time', 'posting times',
 'audience segment', 'audience segments', 'district', 'districts',
 'scheme', 'schemes', 'utility', 'utility types', 'complaint type',
 'complaint types', 'license category', 'license categories',
 'player', 'players', 'match', 'matches', 'event', 'events',
 'training', 'exercise', 'exercises', 'sleep day', 'meal', 'meals',
 'expense category', 'expense categories', 'mood', 'book', 'books',
 'course', 'courses', 'topic', 'topics', 'quiz', 'attempt', 'instructor',
 'instructors', 'skill', 'skills', 'learning mode', 'learning modes',
 'entry', 'entries', 'journal', 'peer', 'certificate', 'certificates']

time_columns=['date', 'dates', 'time', 'times', 'timestamp', 'timestamps', 'datetime', 'datetimes','month', 'months',
              'week', 'weeks', 'day', 'days',
 'quarter', 'quarters', 'year', 'years', 'time slot', 'time slots',
 'date', 'dates', 'season', 'seasons', 'hour', 'hours',
 'posting time', 'posting times', 'training day', 'sleep day',
 'shipment date', 'shipment dates','qtr']

location_terms = {
    "country": [
        "country", "nation", "country_name", "nationality", "sovereign_state",
        "land", "homeland", "country_code", "iso_country", "nation_name",
        "odname", "dev", "world", "continent", "subcontinent", "subregion",
        "member_state", "member_country", "state_party"
    ],
    "city": [
        "city", "town", "municipality", "metro", "metropolis", "urban_area",
        "city_name", "township", "borough", "capital", "village", "urban",
        "metro_area", "conurbation", "settlement", "locality_name"
    ],
    "state": [
        "state", "province", "region", "territory", "governorate", "prefecture",
        "division", "county", "oblast", "subdivision", "federal_state", "administrative_area",
        "state_name", "province_name", "region_name", "territory_name", "governorate_name",
        "prefecture_name", "division_name", "county_name", "oblast_name",
        "state_code", "province_code", "region_code", "territory_code", "governorate_code",
        "prefecture_code", "division_code", "county_code", "oblast_code",
        "state_id", "province_id", "region_id", "territory_id", "governorate_id",
        "prefecture_id", "division_id", "county_id", "oblast_id",
        "state_abbr", "province_abbr", "region_abbr", "territory_abbr", "governorate_abbr",
        "prefecture_abbr", "division_abbr", "county_abbr", "oblast_abbr",
        "state_iso", "province_iso", "region_iso", "territory_iso", "governorate_iso",
        "prefecture_iso", "division_iso", "county_iso", "oblast_iso",
        "reg", "reg_name", "reg_code", "reg_abbr", "reg_iso", "regname",
        "statehood", "admin_region", "admin_division", "state_entity"
    ],
    "area": [
        "area", "district", "locality", "zone", "subzone", "sector",
        "ward", "neighborhood", "region_area", "block", "circle", "areaname",
        "subdistrict", "tehsil", "taluka", "parish", "commune", "borough_area"
    ],
    "postal": [
        "postal","postalcode", "postal_code", "zipcode", "zip", "pin", "pincode",
        "post_code", "mail_code", "zip_code", "postal_number", "postcode",
        "delivery_code", "sorting_code"
    ],
    "address": [
        "address", "street", "street_address", "road", "lane", "avenue", "drive",
        "colony", "apartment", "flat", "building", "house_number", "location",
        "residence", "unit", "plot", "lot", "address_line"
    ],
    "coordinates": [
        "latitude", "lat", "longitude", "lon", "lng", "geo",
        "geo_location", "coordinates", "x_coord", "y_coord", "geocode",
        "latlon", "longlat", "gps", "spatial", "geom"
    ]
}

Numerical_columns=['id','sales', 'revenue', 'growth', 'expense', 'expenses', 'count', 'counts',
 'score', 'scores', 'rating', 'ratings', 'completion', 'attendance',
 'population', 'income', 'performance', 'progress', 'conversion',
 'clicks', 'reach', 'usage', 'crashes', 'crash', 'frequency',
 'GDP', 'engagement', 'vaccinations', 'mortality', 'patients',
 'cases', 'admissions', 'footfall', 'impressions', 'views',
 'capacity', 'volume', 'stats', 'mastery', 'attempts',
 'coverage', 'distribution', 'amount', 'percent', 'percentage',
 'rate', 'rates', 'spent', 'spend', 'return', 'budget', 'budgets',
 'redemption', 'allocation', 'satisfaction', 'like', 'likes',
 'share', 'shares', 'followers', 'follower', 'reach', 'ROI',
 'usage', 'value', 'values', 'lead', 'leads', 'crashes',
 'api calls', 'downloads', 'temperature', 'transactions',
 'visits', 'visitors', 'literacy', 'energy', 'traffic',
 'restock', 'delivery', 'orders', 'stock', 'quantity',
 'damage', 'line', 'code', 'bugs', 'fixed', 'commits',
 'test coverage', 'placed', 'purchases', 'calories',
 'calorie', 'burned', 'speed', 'ranking', 'point', 'points',
 'goals', 'score', 'completed', 'attempts', 'correct',
 'answer', 'difficulty', 'duration', 'productivity',
 'usage', 'conversion', 'engagement', 'impressions','avg','average']

Contact = ["phone","phone_number","mobile","mobile_number","contact","contact_number",
           "telephone","telephone_number","cell","cell_number","phone_no","mobile_no",
           "contact_no","tel_no","primary_phone","secondary_phone","work_phone","home_phone",
           "office_phone","personal_phone","emergency_contact_number"]



df=pd.read_csv('Canada.csv',encoding='unicode_escape')
# df=pd.read_excel("Tableau Joins File.xlsx")
# df=pd.read_json("try.json")

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

for i in alpha_columns:
    df[i]=df[i].str.lower()
    val=df.loc[0,i]
    if (val=="yes") or (val=="no") or (val=="y") or (val=="n"):
        df[i]=df[i].replace({"yes":"Yes","no":"No","y":"Yes","n":"No"})
    elif (val=="true") or (val=="false"):
        df[i]=df[i].replace({"true":"True","false":"False"})
    elif (val=="m") or (val=="f"):
        df[i].replace({"m":"Male","f":"Female"},inplace=True)
    df[i]=df[i].str.title()

for i in alpha_columns:
    df[i]=df[i].fillna("Unknown")
for i in numerical_columns:
    df[i]=df[i].fillna(df[i].median())
for i in location_columns:
    df[i]=df[i].fillna("Unknown")

for i in summary:
    print(f"{i}:-\n{eval(i)}\n")
for i in df.columns:
    print(f"{i}\n{df[i].describe()}\n")
print(df.head())
print(df.tail())

#graph col:-
X_Qualitative=[]
X_Quantitative=[]
X_Location=[]
X_Time=[]

for i in column_name:
    a=len(df[i].unique())
    if a<=15 :
        if i in alpha_columns:
            X_Qualitative.append(i)
        elif i in numerical_columns:
            X_Quantitative.append(i)
        elif i in date_columns:
            X_Time.append(i)
print(X_Qualitative)
print(X_Quantitative)
print(X_Time)

single=[]
N_single=[]
P_single=[]
mix=[]
N_mix=[]
L_mix=[]
P_mix=[]
dia=[single,N_single,P_single,mix,N_mix,L_mix,P_mix]
Dia_ID=[]
Access=[]

# Bar charts>>>
j=0
k=0

for col_index, col_name in enumerate(X_Qualitative):
    unique_vals = df[col_name].unique()
    if len(unique_vals) < 3 or len(unique_vals)>15:
        single.append([])
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
                hoverlabel=dict(bgcolor="white")
            )
            single[j].append([])
            single[j][i].append(fig)
            i=i+1
        j=j+1
    else:
        mix.append([])
        si=0
        for num_col in numerical_columns:
            grouped = df.groupby(col_name)[num_col].sum()
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=grouped.index,
                y=grouped.values,
                text=grouped.values,
                hovertemplate=
                "<b>Category:</b> %{x}<br>" +
                "<b>Value:</b> %{y}<br>" +
                "<extra></extra>"
            ))
            fig.update_layout(
                title=f"{num_col} by {col_name}",
                xaxis_title=col_name,
                yaxis_title=num_col
            )
            mix[k].append([])
            mix[k][si].append(fig)
            si=si+1
        k=k+1

j=0
k=0


for col_index, col_name in enumerate(X_Quantitative):
    unique_vals = df[col_name].unique()
    if len(unique_vals) < 3:
        N_single.append([])
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
                hoverlabel=dict(bgcolor="white")
            )
            N_single[j].append([])
            N_single[j][i].append(fig)
            i=i+1
        j=j+1


    else:
        N_mix.append([])
        si=0
        for num_col in numerical_columns:
            grouped = df.groupby(col_name)[num_col].sum()
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=grouped.index,
                y=grouped.values,
                text=grouped.values,
                hovertemplate=
                "<b>Category:</b> %{x}<br>" +
                "<b>Value:</b> %{y}<br>" +
                "<extra></extra>"
            ))
            fig.update_layout(
                title=f"{num_col} by {col_name}",
                xaxis_title=col_name,
                yaxis_title=num_col
            )
            N_mix[k].append([])
            N_mix[k][si].append(fig)
            si=si+1
        k=k+1

j=0

for col_index, col_name in enumerate(location_columns):
    L_mix.append([])
    si=0
    for num_col in numerical_columns:
        grouped = df.groupby(col_name)[num_col].sum()
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=grouped.index,
            y=grouped.values,
            text=grouped.values,
            hovertemplate=
            "<b>Category:</b> %{x}<br>" +
            "<b>Value:</b> %{y}<br>" +
            "<extra></extra>"
        ))
        fig.update_layout(
            title=f"{num_col} by {col_name}",
            xaxis_title=col_name,
            yaxis_title=num_col
        )
        L_mix[j].append([])
        L_mix[j][si].append(fig)
        si=si+1
    j=j+1

for col_index, col_name in enumerate(X_Time):
    for num_col in numerical_columns:
                grouped = df.groupby(col_name)[num_col].sum()
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=grouped.index,
                    y=grouped.values,
                    text=grouped.values,
                    hovertemplate=
                    "<b>Category:</b> %{x}<br>" +
                    "<b>Value:</b> %{y}<br>" +
                    "<extra></extra>"
                ))
                fig.update_layout(
                    title=f"{num_col} by {col_name}",
                    xaxis_title=col_name,
                    yaxis_title=num_col
                )
                fig.show()
# <-------------------------------------------------------------------------------->

#Pie charts>>>
j=0

for i in column_name:
    si=0
    if len(df[i].unique()) <= 8:
        P_single.append([])
        counts = df[i].value_counts()
        fig = go.Figure()
        fig.add_trace(go.Pie(
            labels=counts.index,
            values=counts.values,
            hole=0.4,
            hovertemplate="<b>%{label}</b><br>Count: %{value}<extra></extra>"
        ))
        fig.update_layout(
            title=f"Distribution of {i}",
            legend_title="Categories"
        )
        P_single[j].append([])
        P_single[j][si].append(fig)
        si=si+1
        j=j+1

j=0
for i in X_Qualitative:
    P_mix.append([])
    for l in numerical_columns:
        si=0
        grouped = df.groupby(i)[l].sum()
        fig = go.Figure()
        fig.add_trace(go.Pie(
            labels=grouped.index,
            values=grouped.values,
            hole=0.4,
            hovertemplate="<b>%{label}</b><br>Value: %{value}<extra></extra>"
        ))

        fig.update_layout(
            title=f"Distribution of {l} by {i}",
            legend_title=i
        )
        P_mix[j].append([])
        P_mix[j][si].append(fig)
        si=si+1
    j=j+1


def ensure_datetime(series):
    try:
        return pd.to_datetime(series, errors='coerce')
    except:
        return series

for d in date_columns:
    df[d] = ensure_datetime(df[d])
    if not pd.api.types.is_datetime64_any_dtype(df[d]):
        continue
    for num_col in numerical_columns:

# Bar Chart (Aggregated by Month/Year)
        df['year'] = df[d].dt.year
        df['month'] = df[d].dt.month

        monthly = df.groupby('month')[num_col].sum().reset_index()
        yearly = df.groupby('year')[num_col].sum().reset_index()

Dia_ID=[]
i=-1
for all in dia:
    i+=1
    for j in range(0,len(all)):
        for k in range(len(all[j])):
            for l in range(len(all[j][k])):
                Dia_ID.append(str(i)+str(j)+str(k)+str(l))
print(Dia_ID)

Access=[]
for i in range(int(max(Dia_ID)[0])+1):
    Access.append([])
    for val in (Dia_ID):
        if val[0]==str(i):
            Access[i].append(val)
Access[:] = [x for x in Access if x]
print(Access)

count=0
for all in dia:
    for i in range(0,len(all)):
        for j in range(len(all[i])):
            for k in range(len(all[i][j])):
                # all[i][j][k].show()
                count+=1
print("Total graphs displayed:",count)

# def ensure_datetime(series):
#     try:
#         return pd.to_datetime(series, errors='coerce')
#     except:
#         return series

# for d in date_columns:
#     df[d] = ensure_datetime(df[d])
#     if not pd.api.types.is_datetime64_any_dtype(df[d]):
#         continue
#     for num_col in numerical_columns:
# # #Line Chart
# #         fig_line = go.Figure()
# #         fig_line.add_trace(go.Scatter(
# #             x=df[d],
# #             y=df[num_col],
# #             mode='lines',
# #             hovertemplate=
# #                 "<b>Date:</b> %{x}<br>" +
# #                 f"<b>{num_col}:</b> %{y}<extra></extra>"
# #         ))
# #         fig_line.update_layout(
# #             title=f"Line Chart: {num_col} over {d}",
# #             xaxis_title=d,
# #             yaxis_title=num_col
# #         )
# #         fig_line.show()
# # Scatter Plot
#         # fig_scatter = go.Figure()
#         # fig_scatter.add_trace(go.Scatter(
#         #     x=df[d],
#         #     y=df[num_col],
#         #     mode='markers',
#         #     hovertemplate=
#         #         "<b>Date:</b> %{x}<br>" +
#         #         f"<b>{num_col}:</b> %{y}<extra></extra>"
#         # ))
#         # fig_scatter.update_layout(
#         #     title=f"Scatter Plot: {num_col} vs {d}",
#         #     xaxis_title=d,
#         #     yaxis_title=num_col
#         # )
#         # fig_scatter.show()
# # Area Chart
#         # fig_area = go.Figure()
#         # fig_area.add_trace(go.Scatter(
#         #     x=df[d],
#         #     y=df[num_col],
#         #     fill='tozeroy',
#         #     mode='lines',
#         #     hovertemplate=
#         #         "<b>Date:</b> %{x}<br>" +
#         #         f"<b>{num_col}:</b> %{y}<extra></extra>"
#         # ))
#         # fig_area.update_layout(
#         #     title=f"Area Chart: {num_col} over {d}",
#         #     xaxis_title=d,
#         #     yaxis_title=num_col
#         # )
#         # fig_area.show()
# # Bar Chart (Aggregated by Month/Year)
#         df['year'] = df[d].dt.year
#         df['month'] = df[d].dt.month

#         monthly = df.groupby('month')[num_col].sum().reset_index()
#         yearly = df.groupby('year')[num_col].sum().reset_index()

# # # Rolling Average Chart (7-day)
# #         df['rolling'] = df[num_col].rolling(7).mean()

# #         fig_roll = go.Figure()
# #         fig_roll.add_trace(go.Scatter(
# #             x=df[d],
# #             y=df['rolling'],
# #             mode="lines",
# #             hovertemplate=
# #                 "<b>Date:</b> %{x}<br>" +
# #                 f"<b>Rolling Avg ({num_col}):</b> %{y}<extra></extra>"
# #         ))
# #         fig_roll.update_layout(
# #             title=f"7-Day Rolling Average of {num_col}",
# #             xaxis_title=d,
# #             yaxis_title=num_col
# #         )
# #         fig_roll.show()