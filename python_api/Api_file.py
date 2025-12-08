from processor import myAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

total_column_count,total_row_count,column_name,null_columns,droped_column,numerical_columns,phone_number_column,alpha_columns,date_columns,location_columns,country,city,state,postal_code,area,address,coordinates,new_cols,shape,org_shape,summary,X_Qualitative,X_Quantitative,X_Location,X_Time,single,N_single,P_single,mix,N_mix,L_mix,P_mix,dia,Dia_ID,Access,df=myAPI()


sidechart=dia[1][0][0][0]

@app.get("/sideplot")
def side_plot():
    fig_json = sidechart.to_plotly_json()   # <--- KEY STEP
    return JSONResponse(content=fig_json)

chart1=dia[1][0][1][0]

@app.get("/chart1plot")
def chart1_plot():
    fig_json = chart1.to_plotly_json()   # <--- KEY STEP
    return JSONResponse(content=fig_json)

chart2=dia[2][0][0][0]

@app.get("/chart2plot")
def chart2_plot():
    fig_json = chart2.to_plotly_json()   # <--- KEY STEP
    return JSONResponse(content=fig_json)

a=df[numerical_columns[0]].sum()
b=df[numerical_columns[1]].sum()
c=df[numerical_columns[2]].sum()
d=df[numerical_columns[3]].sum()
print(Dia_ID)

@app.get("/process")
def process_data():
    

    return {
    "onename":numerical_columns[0],
    "one":int(a),
    "twoname": numerical_columns[1],
    "two": int(b),
    "threename": numerical_columns[2],
    "three":int(c) ,
    "fourname": numerical_columns[3],
    "four": int(d),
    "five": 123,
    "six": 456,
    "seven":789,
    "eight": 101112,
    "summary": summary,
    }