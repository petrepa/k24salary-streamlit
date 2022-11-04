"""
# Kode 24 Salary Streamlit App 💵🤑
A quick data app based on [Kode24's salary statistics](https://www.kode24.no/artikkel/vaer-sa-god-her-er-lonningene-til-over-1200-norske-utviklere/77208900). 

> Den siste utgaven av kode24s lønnsundersøkelse har vist at norske utviklere i snitt tjener 770.000 kroner i året uten bonus, 832.000 kroner med bonus, aller mest i Oslo, mer jo lenger vekk fra koden du sitter og, i alle fall til en viss grad, mer jo høyere utdanning du har.

Inspired by [Einar Eriksen](https://www.linkedin.com/in/einareriksen/)s work.
- [Se hvordan en data scientist knar lønnstallene våre med Python](https://www.kode24.no/artikkel/se-hvordan-en-data-scientist-knar-lonnstallene-vare-med-python/77311832)
- [En kjapp notebook basert på Kode24s lønnsstatistikk](https://colab.research.google.com/drive/1BlubmdD_pBGY9fij3ycSQxKu1aJ4EbzV?usp=sharing)
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

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


"""
## Distribution
As Einar states, salary is rarly a normal distribution. 
Few or nobody gets 500 000 kr less than the average or median salary, 
but alot of people get more. Therefore we get a long tailed distribution.
"""

fig = px.histogram(df, x="salary")

st.plotly_chart(fig, use_container_width=True)
