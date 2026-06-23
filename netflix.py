# IMPORT LIBRARIES
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams["figure.figsize"] = (10, 6)

# LOAD DATASET
df = pd.read_csv("netflix_titles.csv")

# STEP 1: DATA INSPECTION
print("="*50)
print("DATASET SHAPE")
print("="*50)
print(df.shape)
print("\n" + "="*50)
print("DATA TYPES")
print("="*50)
print(df.dtypes)
print("\n" + "="*50)
print("MISSING VALUES")
print("="*50)
print(df.isnull().sum())
print("\n" + "="*50)
print("DUPLICATE ROWS")
print("="*50)
print(df.duplicated().sum())
print("\n" + "="*50)
print("FIRST 5 RECORDS")
print("="*50)
print(df.head())

# STEP 2: DATA CLEANING

# df["director"] = df["director"].fillna("Unknown")
df["cast"] = df["cast"].fillna("Unknown")
df["country"] = df["country"].fillna("Unknown")

df["rating"] = df["rating"].fillna(
    df["rating"].mode()[0]
)
df["date_added"] = (
    df["date_added"]
    .astype(str)
    .str.strip()
)
df["date_added"] = pd.to_datetime(
    df["date_added"],
    format="mixed",
    errors="coerce"
)
df = df.dropna(subset=["date_added"])
df.drop_duplicates(inplace=True)
df["year_added"] = df["date_added"].dt.year
df["month_added"] = df["date_added"].dt.month
print("\n" + "="*50)
print("AFTER CLEANING")
print("="*50)
print(df.isnull().sum())
print("\nNEW SHAPE")
print(df.shape)

# EDA QUESTION 1
# MOVIES VS TV SHOWS
print("\nQUESTION 1")
print("Movies vs TV Shows")
type_count = df["type"].value_counts()
print(type_count)

# EDA QUESTION 2
# TOP COUNTRIES
print("\nQUESTION 2")
print("Top Countries Producing Content")
country_count = (
    df["country"]
    .value_counts()
    .head(10)
)
print(country_count)

# EDA QUESTION 3
# TOP RATINGS
print("\nQUESTION 3")
print("Most Common Ratings")
rating_count = (
    df["rating"]
    .value_counts()
    .head(10)
)
print(rating_count)

# EDA QUESTION 4
# CONTENT BY YEAR
print("\nQUESTION 4")
print("Content Released By Year")
year_count = (
    df["release_year"]
    .value_counts()
    .sort_index()
)
print(year_count.tail(20))

# EDA QUESTION 5
# TOP GENRES
print("\nQUESTION 5")
print("Top Genres")
genres = (
    df["listed_in"]
    .str.split(", ")
    .explode()
)
genre_count = (
    genres
    .value_counts()
    .head(10)
)
print(genre_count)

# VISUALIZATION 1
# MOVIES VS TV SHOWS
plt.figure()
sns.countplot(
    data=df,
    x="type"
)
plt.title("Movies vs TV Shows")
plt.xlabel("Type")
plt.ylabel("Count")
plt.show()

# VISUALIZATION 2
# TOP COUNTRIES
plt.figure()
country_count.plot(
    kind="bar"
)
plt.title("Top 10 Countries")
plt.xlabel("Country")
plt.ylabel("Titles")
plt.show()

# VISUALIZATION 3
# CONTENT OVER YEARS
plt.figure()
year_count.plot()
plt.title("Netflix Content Released Over Years")
plt.xlabel("Year")
plt.ylabel("Count")
plt.show()

# VISUALIZATION 4
# HISTOGRAM
plt.figure()
plt.hist(
    df["release_year"],
    bins=30
)
plt.title("Release Year Distribution")
plt.xlabel("Release Year")
plt.ylabel("Frequency")
plt.show()

# VISUALIZATION 5
# PIE CHART
plt.figure(figsize=(8,8))
type_count.plot(
    kind="pie",
    autopct="%1.1f%%"
)
plt.title("Content Distribution")
plt.ylabel("")
plt.show()

# VISUALIZATION 6
# SCATTER PLOT
movie_df = df[
    df["type"] == "Movie"
].copy()
movie_df["duration_num"] = (
    movie_df["duration"]
    .str.extract(r"(\d+)")
)
movie_df["duration_num"] = pd.to_numeric(
    movie_df["duration_num"],
    errors="coerce"
)
plt.figure()
plt.scatter(
    movie_df["release_year"],
    movie_df["duration_num"],
    alpha=0.5
)
plt.title("Release Year vs Duration")
plt.xlabel("Release Year")
plt.ylabel("Duration (Minutes)")
plt.show()

# VISUALIZATION 7
# HEATMAP
corr = movie_df[
    ["release_year", "duration_num"]
].corr()
plt.figure()
sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm"
)
plt.title("Correlation Heatmap")
plt.show()

# VISUALIZATION 8
# TOP GENRES
plt.figure()
genre_count.plot(
    kind="bar"
)
plt.title("Top 10 Genres")
plt.xlabel("Genre")
plt.ylabel("Count")
plt.show()

# INSIGHTS REPORT
print("\n")
print("="*50)
print("INSIGHTS REPORT")
print("="*50)
print("""
1. Movies significantly outnumber TV Shows on Netflix.
2. The United States contributes the highest amount of content.
3. Drama and International content dominate the platform.
4. Netflix content production increased sharply after 2015.
5. TV-MA is one of the most common ratings,
indicating a strong adult audience.
""")

# MOST SURPRISING FINDING
print("="*50)
print("MOST SURPRISING FINDING")
print("="*50)
print("""
The most surprising finding was the rapid increase
in Netflix content after 2015.
The platform expanded aggressively during this period.
Many countries increased their contribution.
This shows the global growth of streaming services.
""")