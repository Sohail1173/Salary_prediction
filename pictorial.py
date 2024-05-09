import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def categories(cat,cutoff):
  cat_map={}
  for i in range(len(cat)):
    if cat.values[i]>=cutoff:
      cat_map[cat.index[i]]=cat.index[i]
    else:
      cat_map[cat.index[i]]="Other"
  return cat_map

def clean_exp(x):
  if x== "More than 50 years":
    return 50
  if x=="Less than 1 year":
    return 0.5
  return float(x)



def clean_edu(x):
  if "Bachelor’s degree" in x:
    return "Bachelor’s degree"
  if "Master’s degree" in x:
    return "Master’s degree"
  if "Professional degree" in x or "other doctoral " in x:
    return "Post grad"
  return "Less than a Bachelors"

@st.cache_data
def load_data():
  df=pd.read_csv(r"C:\Users\91808\Downloads\stack-overflow-developer-survey-2020\survey_results_public.csv")
  df=df[["Country","EdLevel","YearsCodePro","Employment","ConvertedComp"]]
  df=df[df["ConvertedComp"].notnull()]
  df=df.dropna()
  df=df[df["Employment"]=="Employed full-time"]
  df=df.drop("Employment",axis=1)
  country_map=categories(df["Country"].value_counts(),400)
  df["Country"]=df["Country"].map(country_map)
  df=df[df["ConvertedComp"]<=250000]
  df=df[df["ConvertedComp"]>=10000]
  df=df[df["Country"]!="Others"]

  df["YearsCodePro"]=df["YearsCodePro"].apply(clean_exp)
  df["EdLevel"]=df["EdLevel"].apply(clean_edu)
  df=df.rename({"ConvertedComp":"Salary"},axis=1)
  return df

df=load_data()

def show_explore_page():
  st.title("Software Developer Salary Prediction")
   
  st.write("## Stack overflow Developer survey 2020")

  data=df["Country"].value_counts()

  fig1,ax1=plt.subplots()
  ax1.pie(data,labels=data.index,autopct="%1.1f%%",shadow=True,startangle=90)
  ax1.axis("equal")

  st.write("### Number of data from different countries")

  st.pyplot(fig1)

  st.write("### Man salary based on country")

  data=df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)

  st.write("### Mean Salary based on Experience")

  data=df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
  st.line_chart(data)

if __name__ == "__main__":
  show_explore_page()