"""
# Kode 24 Salary Streamlit App 💵🤑
A quick data app based on [Kode24's salary statistics](https://www.kode24.no/artikkel/vaer-sa-god-her-er-lonningene-til-over-1200-norske-utviklere/77208900). 

> Den siste utgaven av kode24s lønnsundersøkelse har vist at norske utviklere i snitt tjener 770.000 kroner i året uten bonus, 832.000 kroner med bonus, aller mest i Oslo, mer jo lenger vekk fra koden du sitter og, i alle fall til en viss grad, mer jo høyere utdanning du har.

Inspired by [Einar Eriksen](https://www.linkedin.com/in/einareriksen/)s work.
- [Se hvordan en data scientist knar lønnstallene våre med Python](https://www.kode24.no/artikkel/se-hvordan-en-data-scientist-knar-lonnstallene-vare-med-python/77311832)
- [En kjapp notebook basert på Kode24s lønnsstatistikk](https://colab.research.google.com/drive/1BlubmdD_pBGY9fij3ycSQxKu1aJ4EbzV?usp=sharing)
"""


import numpy as np
import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt
from plotly import express as px
from plotly import graph_objects as go

st.title("Kode 24 Salary Streamlit App 💵🤑")

st.markdown(
    """
    Inspired by [Einar Eriksens](https://www.linkedin.com/in/einareriksen/) [notbook](https://colab.research.google.com/drive/1BlubmdD_pBGY9fij3ycSQxKu1aJ4EbzV?usp=sharing#scrollTo=Kem7cTiP-JqL)
     we will try to analyse the data from the 
    [salary statics](https://www.kode24.no/artikkel/vaer-sa-god-her-er-lonningene-til-over-1200-norske-utviklere/77208900) 
    provided by [Kode24](https://www.kode24.no/).
    """
)

df = pd.read_csv(
    "https://raw.githubusercontent.com/HaliaeetusAlbicilla/k24salary/master/kode24salary.csv"
)

df.columns = [
    "age",
    "education",
    "experience",
    "work_situation",
    "county",
    "work_field",
    "salary",
    "bonus",
    "satisfied",
]

"Where the people work:"

value = df.work_situation.value_counts()
value

# Data cleanup
df[["age_min", "age_max"]] = df["age"].str.split("-", n=1, expand=True)
df.salary = df.salary.str.replace(" kr", "")
df.salary = df.salary.str.replace(",", ".")
df.salary = df.salary.str.replace(" ", "")
df.salary = df.salary.astype(float)

" # Understanding the data "
string = """\
    ## Extremes
    Let's see what the extreme value of the data set is.
    ### Lowest salary
    If we search through the smallest value in the set we get: {lowest}
   """.format(
    lowest=df.salary.min()
)
st.markdown(string)

string = """\
    ### Highest salary
    If we search through the biggest value in the set we get: {highest}
   """.format(
    highest=df.salary.max()
)
st.markdown(string)

string = """\
    ### General measures
    And lastly we also need to find some general measures.
    
    Average: {average}
    
    Median: {median}
   """.format(
    average=df.salary.mean(), median=df.salary.median()
)
st.markdown(string)

st.dataframe(df.describe().T)


"""
## Distribution
As Einar states, salary is rarly a normal distribution. 
Few or nobody gets 500 000 kr less than the average or median salary, 
but alot of people get more. Therefore we get a long tailed distribution.
"""

fig = px.histogram(df, x="salary")

st.plotly_chart(fig, use_container_width=True)

df.experience = df.experience.str.replace(",", ".")
df.experience = df.experience.astype(float)

df.dtypes

dff = (
    df.groupby("work_situation")
    .agg({"salary": ["mean", "median", "count"], "experience": ["mean"]})
    .reset_index()
)

dff.columns = [
    "work_situation",
    "salary_mean",
    "salary_median",
    "work_situation_count",
    "experience_mean",
]

dff

y = dff.salary_median
y.index = dff.work_situation

fig = go.Figure()

fig.add_trace(
    go.Bar(
        name="Median",
        x=y.index,
        y=y,
        hovertemplate="<i>Salary</i>: NOK %{y:.0f} <br><i>Group</i>: %{x}",
    )
)

y = dff.salary_mean
y.index = dff.work_situation

fig.add_trace(
    go.Bar(
        name="Gjennomsnitt",
        x=y.index,
        y=y,
        hovertemplate="<i>Salary</i>: NOK %{y:.0f} <br><i>Group</i>: %{x}",
    )
)
# Text
fig.update_layout(
    yaxis_title="Yearly salary in NOK",
    legend_title="Measures",
    title="Salary per work situation",
)

st.plotly_chart(fig, use_container_width=True)

fig = px.scatter(
    dff,
    x="experience_mean",
    y="salary_mean",
    size="work_situation_count",
    color="work_situation",
    log_x=True,
    size_max=100,
)

# Text
fig.update_layout(
    yaxis_title="Mean salary",
    legend_title="Work situation",
    title="Scatter of salary mean to years of experience",
)

st.plotly_chart(fig)

fig = go.Figure(
    data=[
        go.Box(
            name="Salary",
            x=df.work_situation,
            y=df.salary,
        ),
    ]
)

fig.update_layout(
    yaxis_tickformat=",",
    hoverlabel=dict(
        font_size=14,
    ),
    xaxis_title="Work situation",
    yaxis_title="Salary",
    title="Work situation and salaries",
)

st.plotly_chart(fig)
# figwrite("work_situation_box")
