# Pandas Vignette

March 30, 2022

Vignette: Pandas, reading csv, DataFrames, filtering, and wrangling data

@author: Oscar A. Trevizo

### References
1. "Pandas General Functions" (accessed Feb. 20, 2022) 
    https://pandas.pydata.org/pandas-docs/stable/reference/general_functions.html
    https://pandas.pydata.org/docs/reference/io.html
    https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
1. "Kaggle" (accessed Mar. 20, 2022)
    https://www.kaggle.com/
    https://www.kaggle.com/datasets/rishidamarla/fifa-players-ratings
1. UCI Machine Learning Repository 
    https://archive.ics.uci.edu/ml/datasets.php
1. Additional references:
    https://stackoverflow.com/tags/pandas/
    https://www.w3schools.com/python/pandas/default.asp
    https://www.geeksforgeeks.org/pandas-tutorial/



# Pandas


## Import libraries


```python
import pandas as pd
import numpy as np
```

## Load data from a csv


```python
# https://www.kaggle.com/datasets/rishidamarla/fifa-players-ratings
# And specify which columns to load
df = pd.read_csv('fifa_cleaned.csv')
```


```python
df.shape
```




    (17954, 92)




```python
# https://www.kaggle.com/datasets/rishidamarla/fifa-players-ratings
# And specify which columns to load
df = pd.read_csv('fifa_cleaned.csv', usecols = ['id', 'name', 'birth_date', 'age',
                                                'height_cm', 'weight_kgs', 'positions',
                                                'club_team', 'national_team', 'overall_rating',
                                                'wage_euro'])
```


```python
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>name</th>
      <th>birth_date</th>
      <th>age</th>
      <th>height_cm</th>
      <th>weight_kgs</th>
      <th>positions</th>
      <th>overall_rating</th>
      <th>wage_euro</th>
      <th>club_team</th>
      <th>national_team</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>158023</td>
      <td>L. Messi</td>
      <td>1987-06-24</td>
      <td>31</td>
      <td>170.18</td>
      <td>72.1</td>
      <td>CF,RW,ST</td>
      <td>94</td>
      <td>565000.0</td>
      <td>FC Barcelona</td>
      <td>Argentina</td>
    </tr>
    <tr>
      <th>1</th>
      <td>190460</td>
      <td>C. Eriksen</td>
      <td>1992-02-14</td>
      <td>27</td>
      <td>154.94</td>
      <td>76.2</td>
      <td>CAM,RM,CM</td>
      <td>88</td>
      <td>205000.0</td>
      <td>Tottenham Hotspur</td>
      <td>Denmark</td>
    </tr>
    <tr>
      <th>2</th>
      <td>195864</td>
      <td>P. Pogba</td>
      <td>1993-03-15</td>
      <td>25</td>
      <td>190.50</td>
      <td>83.9</td>
      <td>CM,CAM</td>
      <td>88</td>
      <td>255000.0</td>
      <td>Manchester United</td>
      <td>France</td>
    </tr>
    <tr>
      <th>3</th>
      <td>198219</td>
      <td>L. Insigne</td>
      <td>1991-06-04</td>
      <td>27</td>
      <td>162.56</td>
      <td>59.0</td>
      <td>LW,ST</td>
      <td>88</td>
      <td>165000.0</td>
      <td>Napoli</td>
      <td>Italy</td>
    </tr>
    <tr>
      <th>4</th>
      <td>201024</td>
      <td>K. Koulibaly</td>
      <td>1991-06-20</td>
      <td>27</td>
      <td>187.96</td>
      <td>88.9</td>
      <td>CB</td>
      <td>88</td>
      <td>135000.0</td>
      <td>Napoli</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.shape
```




    (17954, 11)




```python
df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 17954 entries, 0 to 17953
    Data columns (total 11 columns):
     #   Column          Non-Null Count  Dtype  
    ---  ------          --------------  -----  
     0   id              17954 non-null  int64  
     1   name            17954 non-null  object 
     2   birth_date      17954 non-null  object 
     3   age             17954 non-null  int64  
     4   height_cm       17954 non-null  float64
     5   weight_kgs      17954 non-null  float64
     6   positions       17954 non-null  object 
     7   overall_rating  17954 non-null  int64  
     8   wage_euro       17708 non-null  float64
     9   club_team       17940 non-null  object 
     10  national_team   857 non-null    object 
    dtypes: float64(3), int64(3), object(5)
    memory usage: 1.5+ MB
    


```python
# describe statistics
df.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>age</th>
      <th>height_cm</th>
      <th>weight_kgs</th>
      <th>overall_rating</th>
      <th>wage_euro</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>17954.000000</td>
      <td>17954.000000</td>
      <td>17954.000000</td>
      <td>17954.000000</td>
      <td>17954.000000</td>
      <td>17708.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>215411.087780</td>
      <td>25.565445</td>
      <td>174.946921</td>
      <td>75.301047</td>
      <td>66.240169</td>
      <td>9902.134628</td>
    </tr>
    <tr>
      <th>std</th>
      <td>29758.387106</td>
      <td>4.705708</td>
      <td>14.029449</td>
      <td>7.083684</td>
      <td>6.963730</td>
      <td>21995.593750</td>
    </tr>
    <tr>
      <th>min</th>
      <td>16.000000</td>
      <td>17.000000</td>
      <td>152.400000</td>
      <td>49.900000</td>
      <td>47.000000</td>
      <td>1000.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>201117.250000</td>
      <td>22.000000</td>
      <td>154.940000</td>
      <td>69.900000</td>
      <td>62.000000</td>
      <td>1000.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>222919.000000</td>
      <td>25.000000</td>
      <td>175.260000</td>
      <td>74.800000</td>
      <td>66.000000</td>
      <td>3000.000000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>237613.500000</td>
      <td>29.000000</td>
      <td>185.420000</td>
      <td>79.800000</td>
      <td>71.000000</td>
      <td>9000.000000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>247607.000000</td>
      <td>46.000000</td>
      <td>205.740000</td>
      <td>110.200000</td>
      <td>94.000000</td>
      <td>565000.000000</td>
    </tr>
  </tbody>
</table>
</div>



## Filters


```python
# %% Filter basics
#
# A filter is based on a boolean test that returns True or False
#
df['wage_euro'] >= 3000
```




    0         True
    1         True
    2         True
    3         True
    4         True
             ...  
    17949     True
    17950    False
    17951    False
    17952     True
    17953    False
    Name: wage_euro, Length: 17954, dtype: bool




```python
# %% 1st Approach - Filter simple approach
# The boolean test, True or False can be applied to each row
# Get players with wages above the 50 percentile
df_wage_gt_3K = df[df['wage_euro'] >= 3000]
df_wage_gt_3K.shape
```




    (10216, 11)




```python
# Show top 5 using sort_values by wage and head
df_wage_gt_3K.sort_values(by=['wage_euro'], ascending=False).head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>name</th>
      <th>birth_date</th>
      <th>age</th>
      <th>height_cm</th>
      <th>weight_kgs</th>
      <th>positions</th>
      <th>overall_rating</th>
      <th>wage_euro</th>
      <th>club_team</th>
      <th>national_team</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>158023</td>
      <td>L. Messi</td>
      <td>1987-06-24</td>
      <td>31</td>
      <td>170.18</td>
      <td>72.1</td>
      <td>CF,RW,ST</td>
      <td>94</td>
      <td>565000.0</td>
      <td>FC Barcelona</td>
      <td>Argentina</td>
    </tr>
    <tr>
      <th>17938</th>
      <td>176580</td>
      <td>L. Suárez</td>
      <td>1987-01-24</td>
      <td>32</td>
      <td>182.88</td>
      <td>86.2</td>
      <td>ST</td>
      <td>91</td>
      <td>455000.0</td>
      <td>FC Barcelona</td>
      <td>Uruguay</td>
    </tr>
    <tr>
      <th>17939</th>
      <td>177003</td>
      <td>L. Modrić</td>
      <td>1985-09-09</td>
      <td>33</td>
      <td>172.72</td>
      <td>66.2</td>
      <td>CM</td>
      <td>91</td>
      <td>420000.0</td>
      <td>Real Madrid</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>17944</th>
      <td>20801</td>
      <td>Cristiano Ronaldo</td>
      <td>1985-02-05</td>
      <td>34</td>
      <td>187.96</td>
      <td>83.0</td>
      <td>ST,LW</td>
      <td>94</td>
      <td>405000.0</td>
      <td>Juventus</td>
      <td>Portugal</td>
    </tr>
    <tr>
      <th>17924</th>
      <td>173731</td>
      <td>G. Bale</td>
      <td>1989-07-16</td>
      <td>29</td>
      <td>185.42</td>
      <td>82.1</td>
      <td>RW,LW,ST</td>
      <td>88</td>
      <td>355000.0</td>
      <td>Real Madrid</td>
      <td>Wales</td>
    </tr>
  </tbody>
</table>
</div>




```python
# %% Filter select columns and sort one step
#
filter_boolean = df['wage_euro'] >= 3000
# Make a list of column headers
specific_columns = ['name', 'wage_euro', 'club_team', 'national_team']
# Then assign that list to the dataframe and use the boolean to select only true
df_wage_50_less_columns = df[specific_columns][filter_boolean].sort_values(by=['wage_euro'], ascending=False)
df_wage_50_less_columns.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>wage_euro</th>
      <th>club_team</th>
      <th>national_team</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>L. Messi</td>
      <td>565000.0</td>
      <td>FC Barcelona</td>
      <td>Argentina</td>
    </tr>
    <tr>
      <th>17938</th>
      <td>L. Suárez</td>
      <td>455000.0</td>
      <td>FC Barcelona</td>
      <td>Uruguay</td>
    </tr>
    <tr>
      <th>17939</th>
      <td>L. Modrić</td>
      <td>420000.0</td>
      <td>Real Madrid</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>17944</th>
      <td>Cristiano Ronaldo</td>
      <td>405000.0</td>
      <td>Juventus</td>
      <td>Portugal</td>
    </tr>
    <tr>
      <th>17924</th>
      <td>G. Bale</td>
      <td>355000.0</td>
      <td>Real Madrid</td>
      <td>Wales</td>
    </tr>
  </tbody>
</table>
</div>




```python
# %% Filter multiple conditions
#
# Apply two conditions. Get players with wages above the 50 percentile, and national team is Brazil
#
df_wage_50_brazil = df[(df['wage_euro'] >= 3000) & (df['national_team'] == 'Brazil')]
df_wage_50_brazil.shape
```




    (23, 11)




```python
# Show top 5 using sort_values by wage and head
df_wage_50_brazil.sort_values(by=['wage_euro'], ascending=False).head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>name</th>
      <th>birth_date</th>
      <th>age</th>
      <th>height_cm</th>
      <th>weight_kgs</th>
      <th>positions</th>
      <th>overall_rating</th>
      <th>wage_euro</th>
      <th>club_team</th>
      <th>national_team</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>17943</th>
      <td>190871</td>
      <td>Neymar Jr</td>
      <td>1992-02-05</td>
      <td>27</td>
      <td>175.26</td>
      <td>68.0</td>
      <td>LW,CAM</td>
      <td>92</td>
      <td>290000.0</td>
      <td>Paris Saint-Germain</td>
      <td>Brazil</td>
    </tr>
    <tr>
      <th>17833</th>
      <td>230294</td>
      <td>Louri Beretta</td>
      <td>1992-02-29</td>
      <td>27</td>
      <td>187.96</td>
      <td>83.0</td>
      <td>ST,CF</td>
      <td>83</td>
      <td>60000.0</td>
      <td>Atlético Mineiro</td>
      <td>Brazil</td>
    </tr>
    <tr>
      <th>17835</th>
      <td>230481</td>
      <td>Ronaldo Cabrais</td>
      <td>1992-02-29</td>
      <td>27</td>
      <td>152.40</td>
      <td>74.8</td>
      <td>RW,CAM</td>
      <td>83</td>
      <td>51000.0</td>
      <td>Grêmio</td>
      <td>Brazil</td>
    </tr>
    <tr>
      <th>76</th>
      <td>230258</td>
      <td>Rosberto Dourado</td>
      <td>1988-02-29</td>
      <td>31</td>
      <td>175.26</td>
      <td>69.9</td>
      <td>CDM,CM</td>
      <td>82</td>
      <td>46000.0</td>
      <td>Atlético Mineiro</td>
      <td>Brazil</td>
    </tr>
    <tr>
      <th>17834</th>
      <td>230375</td>
      <td>Josué Chiamulera</td>
      <td>1992-02-29</td>
      <td>27</td>
      <td>185.42</td>
      <td>79.8</td>
      <td>CB</td>
      <td>83</td>
      <td>43000.0</td>
      <td>Grêmio</td>
      <td>Brazil</td>
    </tr>
  </tbody>
</table>
</div>




```python
# %% Filter unique select one columns (a list)
#
# Need 
filter_boolean = df['wage_euro'] >= 3000
# Then assign that list to the dataframe and use the boolean to select only true
# And dropna()
df_top_natl_tm = df['national_team'][filter_boolean].dropna()

df_top_natl_tm = df_top_natl_tm.unique()    # returns a numpy array series
type(df_top_natl_tm)
```




    numpy.ndarray




```python
# Displaying the numpy array series
df_top_natl_tm
```




    array(['Argentina', 'Denmark', 'France', 'Italy', 'Netherlands',
           'Germany', 'Uruguay', 'Spain', 'Belgium', 'Egypt', 'Colombia',
           'Sporting CP', 'Portugal', 'Dalian YiFang FC', 'Mexico', 'Brazil',
           'England', 'Austria', 'Al Hilal', 'Iceland', 'Hungary', 'Wales',
           'Cameroon', "Côte d'Ivoire", 'Australia', 'FC Porto', 'Romania',
           'Chile', 'Norway', 'Venezuela', 'Sweden', 'Scotland', 'Canada',
           'SL Benfica', 'Poland', 'Turkey', 'Northern Ireland',
           'Santos Laguna', 'New Zealand', 'United States',
           'Republic of Ireland', 'Ecuador', 'Pachuca', 'Peru', 'Slovenia',
           'Racing Club', 'FC Red Bull Salzburg', 'Puebla FC',
           'Universidad de Chile', 'Club Tijuana', 'Paraguay', 'Querétaro',
           'South Africa', 'Cruz Azul', 'Switzerland', 'BSC Young Boys',
           'Atlético Nacional', 'Finland', 'Melbourne Victory',
           'Independiente Santa Fe', 'Melbourne City FC',
           'Club Atlético Talleres', 'Urawa Red Diamonds', 'Al Ahli',
           'FK Austria Wien', 'Al Wehda', 'Bulgaria', 'Monarcas Morelia',
           'Sydney FC', 'Club Atlas', 'Al Ittihad', 'Boca Juniors',
           'Vélez Sarsfield', 'CD Tondela', 'Colo-Colo', 'Czech Republic',
           'Club Necaxa', 'Perth Glory', 'Western Sydney Wanderers',
           'Nagoya Grampus', 'FC Basel 1893', 'Greece', 'Club León',
           'Club Atlético Banfield', 'Russia', 'Club América',
           'Tigres U.A.N.L.', 'Independiente', 'Monterrey', 'Henan Jianye FC',
           'Grasshopper Club Zürich', 'Neuchâtel Xamax', 'SK Rapid Wien',
           'Vitória Guimarães', 'Junior FC', 'River Plate'], dtype=object)




```python
# Convert numpy array to Pandas series
df_top_natl_tm = pd.Series(df_top_natl_tm)
type(df_top_natl_tm)
```




    pandas.core.series.Series




```python
df_top_natl_tm.head()
```




    0      Argentina
    1        Denmark
    2         France
    3          Italy
    4    Netherlands
    dtype: object



## Create a DataFrame


```python
# Get the data
first_name = [" Joan", "Mary ", " Vijay ", "Rob ", "Martha", "Josh", " Vicky", " Mario", "Jenny", "Joe"]
last_name = [" T"," K ", " N ", "R ", "L", "F ", " R", " L", "%^", "P"]
score_1 = [91, 83, 95, 72, 91, 85, 89, 82, 'abc', 79]
score_2 = [91, 85, 90, 81, 95, 92, 88, 94, 'xyz', 75]

# Build the dataframe
df = pd.DataFrame({'first_name':first_name, 'last_name':last_name,'score_1':score_1,'score_2':score_2}  )
df.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>first_name</th>
      <th>last_name</th>
      <th>score_1</th>
      <th>score_2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Joan</td>
      <td>T</td>
      <td>91</td>
      <td>91</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Mary</td>
      <td>K</td>
      <td>83</td>
      <td>85</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Vijay</td>
      <td>N</td>
      <td>95</td>
      <td>90</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Rob</td>
      <td>R</td>
      <td>72</td>
      <td>81</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Martha</td>
      <td>L</td>
      <td>91</td>
      <td>95</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Josh</td>
      <td>F</td>
      <td>85</td>
      <td>92</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Vicky</td>
      <td>R</td>
      <td>89</td>
      <td>88</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Mario</td>
      <td>L</td>
      <td>82</td>
      <td>94</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Jenny</td>
      <td>%^</td>
      <td>abc</td>
      <td>xyz</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Joe</td>
      <td>P</td>
      <td>79</td>
      <td>75</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 10 entries, 0 to 9
    Data columns (total 4 columns):
     #   Column      Non-Null Count  Dtype 
    ---  ------      --------------  ----- 
     0   first_name  10 non-null     object
     1   last_name   10 non-null     object
     2   score_1     10 non-null     object
     3   score_2     10 non-null     object
    dtypes: object(4)
    memory usage: 448.0+ bytes
    

## To numeric


```python
df['score_1'] = pd.to_numeric(df['score_1'], errors='coerce')
```


```python
df['score_2'] = pd.to_numeric(df['score_2'], errors='coerce')
```


```python
df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 10 entries, 0 to 9
    Data columns (total 4 columns):
     #   Column      Non-Null Count  Dtype  
    ---  ------      --------------  -----  
     0   first_name  10 non-null     object 
     1   last_name   10 non-null     object 
     2   score_1     9 non-null      float64
     3   score_2     9 non-null      float64
    dtypes: float64(2), object(2)
    memory usage: 448.0+ bytes
    


```python
df.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>score_1</th>
      <th>score_2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>9.000000</td>
      <td>9.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>85.222222</td>
      <td>87.888889</td>
    </tr>
    <tr>
      <th>std</th>
      <td>7.120003</td>
      <td>6.527719</td>
    </tr>
    <tr>
      <th>min</th>
      <td>72.000000</td>
      <td>75.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>82.000000</td>
      <td>85.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>85.000000</td>
      <td>90.000000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>91.000000</td>
      <td>92.000000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>95.000000</td>
      <td>95.000000</td>
    </tr>
  </tbody>
</table>
</div>



## Clean up blank spaces


```python
# Strip right and left spaces
df["first_name"] = df["first_name"].str.strip()
df["last_name"] = df["last_name"].str.strip()
df.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>first_name</th>
      <th>last_name</th>
      <th>score_1</th>
      <th>score_2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Joan</td>
      <td>T</td>
      <td>91.0</td>
      <td>91.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Mary</td>
      <td>K</td>
      <td>83.0</td>
      <td>85.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Vijay</td>
      <td>N</td>
      <td>95.0</td>
      <td>90.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Rob</td>
      <td>R</td>
      <td>72.0</td>
      <td>81.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Martha</td>
      <td>L</td>
      <td>91.0</td>
      <td>95.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Josh</td>
      <td>F</td>
      <td>85.0</td>
      <td>92.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Vicky</td>
      <td>R</td>
      <td>89.0</td>
      <td>88.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Mario</td>
      <td>L</td>
      <td>82.0</td>
      <td>94.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Jenny</td>
      <td>%^</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Joe</td>
      <td>P</td>
      <td>79.0</td>
      <td>75.0</td>
    </tr>
  </tbody>
</table>
</div>



## Regex clean up characters
http://localhost:8888/notebooks/Python/Jupyter_Vignettes/regex_vignette.ipynb


```python
df["last_name"] = df["last_name"].replace('[^A-Za-z]', np.NaN, regex=True)
df["score_1"] = df["score_1"].replace('[^0-9]', np.NaN, regex=True)
df["score_2"] = df["score_2"].replace('[^0-9]', np.NaN, regex=True)

df.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>first_name</th>
      <th>last_name</th>
      <th>score_1</th>
      <th>score_2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Joan</td>
      <td>T</td>
      <td>91.0</td>
      <td>91.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Mary</td>
      <td>K</td>
      <td>83.0</td>
      <td>85.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Vijay</td>
      <td>N</td>
      <td>95.0</td>
      <td>90.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Rob</td>
      <td>R</td>
      <td>72.0</td>
      <td>81.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Martha</td>
      <td>L</td>
      <td>91.0</td>
      <td>95.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Josh</td>
      <td>F</td>
      <td>85.0</td>
      <td>92.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Vicky</td>
      <td>R</td>
      <td>89.0</td>
      <td>88.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Mario</td>
      <td>L</td>
      <td>82.0</td>
      <td>94.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Jenny</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Joe</td>
      <td>P</td>
      <td>79.0</td>
      <td>75.0</td>
    </tr>
  </tbody>
</table>
</div>



## Drop NaN


```python
df.dropna(inplace=True)
df.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>first_name</th>
      <th>last_name</th>
      <th>score_1</th>
      <th>score_2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Joan</td>
      <td>T</td>
      <td>91.0</td>
      <td>91.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Mary</td>
      <td>K</td>
      <td>83.0</td>
      <td>85.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Vijay</td>
      <td>N</td>
      <td>95.0</td>
      <td>90.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Rob</td>
      <td>R</td>
      <td>72.0</td>
      <td>81.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Martha</td>
      <td>L</td>
      <td>91.0</td>
      <td>95.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Josh</td>
      <td>F</td>
      <td>85.0</td>
      <td>92.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Vicky</td>
      <td>R</td>
      <td>89.0</td>
      <td>88.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Mario</td>
      <td>L</td>
      <td>82.0</td>
      <td>94.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Joe</td>
      <td>P</td>
      <td>79.0</td>
      <td>75.0</td>
    </tr>
  </tbody>
</table>
</div>



## Assign data types


```python
df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 9 entries, 0 to 9
    Data columns (total 4 columns):
     #   Column      Non-Null Count  Dtype  
    ---  ------      --------------  -----  
     0   first_name  9 non-null      object 
     1   last_name   9 non-null      object 
     2   score_1     9 non-null      float64
     3   score_2     9 non-null      float64
    dtypes: float64(2), object(2)
    memory usage: 360.0+ bytes
    


```python
# Based on example from https://www.geeksforgeeks.org/change-data-type-for-one-or-more-columns-in-pandas-dataframe
# Similar reference in https://stackoverflow.com/questions/49684951/pandas-read-csv-dtype-read-all-columns-but-few-as-string
dtypes_dict = {'first_name' : str,
               'last_name' : str,
               'score_1' : int,
               'score_2' : int}
df = df.astype(dtypes_dict)
```


```python
df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 9 entries, 0 to 9
    Data columns (total 4 columns):
     #   Column      Non-Null Count  Dtype 
    ---  ------      --------------  ----- 
     0   first_name  9 non-null      object
     1   last_name   9 non-null      object
     2   score_1     9 non-null      int32 
     3   score_2     9 non-null      int32 
    dtypes: int32(2), object(2)
    memory usage: 288.0+ bytes
    

## Add column / List comprehension


```python
df['s1_a'] = ['a' if col >= 90 else ' ' for col in df['score_1']]
```


```python
df.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>first_name</th>
      <th>last_name</th>
      <th>score_1</th>
      <th>score_2</th>
      <th>s1_a</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Joan</td>
      <td>T</td>
      <td>91</td>
      <td>91</td>
      <td>a</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Mary</td>
      <td>K</td>
      <td>83</td>
      <td>85</td>
      <td></td>
    </tr>
    <tr>
      <th>2</th>
      <td>Vijay</td>
      <td>N</td>
      <td>95</td>
      <td>90</td>
      <td>a</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Rob</td>
      <td>R</td>
      <td>72</td>
      <td>81</td>
      <td></td>
    </tr>
    <tr>
      <th>4</th>
      <td>Martha</td>
      <td>L</td>
      <td>91</td>
      <td>95</td>
      <td>a</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Josh</td>
      <td>F</td>
      <td>85</td>
      <td>92</td>
      <td></td>
    </tr>
    <tr>
      <th>6</th>
      <td>Vicky</td>
      <td>R</td>
      <td>89</td>
      <td>88</td>
      <td></td>
    </tr>
    <tr>
      <th>7</th>
      <td>Mario</td>
      <td>L</td>
      <td>82</td>
      <td>94</td>
      <td></td>
    </tr>
    <tr>
      <th>9</th>
      <td>Joe</td>
      <td>P</td>
      <td>79</td>
      <td>75</td>
      <td></td>
    </tr>
  </tbody>
</table>
</div>




```python
df['s2_a'] = ['a' if col >= 90 else ' ' for col in df['score_2']]
```


```python
df.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>first_name</th>
      <th>last_name</th>
      <th>score_1</th>
      <th>score_2</th>
      <th>s1_a</th>
      <th>s2_a</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Joan</td>
      <td>T</td>
      <td>91</td>
      <td>91</td>
      <td>a</td>
      <td>a</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Mary</td>
      <td>K</td>
      <td>83</td>
      <td>85</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2</th>
      <td>Vijay</td>
      <td>N</td>
      <td>95</td>
      <td>90</td>
      <td>a</td>
      <td>a</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Rob</td>
      <td>R</td>
      <td>72</td>
      <td>81</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>4</th>
      <td>Martha</td>
      <td>L</td>
      <td>91</td>
      <td>95</td>
      <td>a</td>
      <td>a</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Josh</td>
      <td>F</td>
      <td>85</td>
      <td>92</td>
      <td></td>
      <td>a</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Vicky</td>
      <td>R</td>
      <td>89</td>
      <td>88</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>7</th>
      <td>Mario</td>
      <td>L</td>
      <td>82</td>
      <td>94</td>
      <td></td>
      <td>a</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Joe</td>
      <td>P</td>
      <td>79</td>
      <td>75</td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>
</div>




```python
df['improved'] = ['yes' if col2 > col1 else 'no' for col1, col2 in zip(df['score_1'], df['score_2'])]
```


```python
df.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>first_name</th>
      <th>last_name</th>
      <th>score_1</th>
      <th>score_2</th>
      <th>s1_a</th>
      <th>s2_a</th>
      <th>improved</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Joan</td>
      <td>T</td>
      <td>91</td>
      <td>91</td>
      <td>a</td>
      <td>a</td>
      <td>no</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Mary</td>
      <td>K</td>
      <td>83</td>
      <td>85</td>
      <td></td>
      <td></td>
      <td>yes</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Vijay</td>
      <td>N</td>
      <td>95</td>
      <td>90</td>
      <td>a</td>
      <td>a</td>
      <td>no</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Rob</td>
      <td>R</td>
      <td>72</td>
      <td>81</td>
      <td></td>
      <td></td>
      <td>yes</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Martha</td>
      <td>L</td>
      <td>91</td>
      <td>95</td>
      <td>a</td>
      <td>a</td>
      <td>yes</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Josh</td>
      <td>F</td>
      <td>85</td>
      <td>92</td>
      <td></td>
      <td>a</td>
      <td>yes</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Vicky</td>
      <td>R</td>
      <td>89</td>
      <td>88</td>
      <td></td>
      <td></td>
      <td>no</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Mario</td>
      <td>L</td>
      <td>82</td>
      <td>94</td>
      <td></td>
      <td>a</td>
      <td>yes</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Joe</td>
      <td>P</td>
      <td>79</td>
      <td>75</td>
      <td></td>
      <td></td>
      <td>no</td>
    </tr>
  </tbody>
</table>
</div>



##  Filter addl examples


```python
# The filter itself
df["score_1"] == df.score_1.max()
```




    0    False
    1    False
    2     True
    3    False
    4    False
    5    False
    6    False
    7    False
    9    False
    Name: score_1, dtype: bool




```python
# The filter applied, and to certain columns only
df[['first_name', 'last_name','score_1']][df["score_1"] == df.score_1.max()]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>first_name</th>
      <th>last_name</th>
      <th>score_1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2</th>
      <td>Vijay</td>
      <td>N</td>
      <td>95</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Another filter, applied, for practice
df[['first_name', 'last_name','score_1', 'score_2']][(df["score_1"] > 90) & (df['score_2'] > 90) ]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>first_name</th>
      <th>last_name</th>
      <th>score_1</th>
      <th>score_2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Joan</td>
      <td>T</td>
      <td>91</td>
      <td>91</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Martha</td>
      <td>L</td>
      <td>91</td>
      <td>95</td>
    </tr>
  </tbody>
</table>
</div>


