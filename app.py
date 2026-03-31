import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title("TikTok vs Spotify: What Makes a Song Go Viral?")
st.write("An analysis of 3,560 TikTok trending tracks and 4,370 top Spotify songs")

# Load data
df_tiktok=pd.read_csv('tiktok.csv')
df_tiktok= df_tiktok.drop_duplicates(subset='track_id')

df_spotify = pd.read_csv('Most Streamed Spotify Songs 2024.csv', encoding='latin-1')
df_spotify= df_spotify.drop_duplicates(subset='Track')

st.write(f"TikTok dataset: {df_tiktok.shape[0]} songs")
st.write(f"Spotify dataset: {df_spotify.shape[0]} songs")

# Clean Spotify data
tiktok_cols= ['Spotify Streams', 'Spotify Popularity', 'TikTok Views', 'TikTok Likes', 'TikTok Posts']

for col in tiktok_cols:
    df_spotify[col]= pd.to_numeric(
        df_spotify[col].astype(str).str.replace(',', ''),
        errors='coerce'
    )

df_spotify['TikTok Views'] = df_spotify['TikTok Views'].fillna(0)
df_spotify['TikTok Likes'] = df_spotify['TikTok Likes'].fillna(0)
df_spotify['TikTok Posts'] = df_spotify['TikTok Posts'].fillna(0)

# Create Platform categories
df_spotify['combined_score']=(
    df_spotify['TikTok Views'] / df_spotify['TikTok Views'].max()+df_spotify['Spotify Streams'] / df_spotify['Spotify Streams'].max()
)
df_spotify['tiktok_viral']= (df_spotify['TikTok Views'] > df_spotify['TikTok Views'].quantile(0.75)).astype(int)
df_spotify['spotify_dominant'] = (df_spotify['Spotify Streams'] > df_spotify['Spotify Streams'].quantile(0.75)).astype(int)

def categorize(row):
    if row['tiktok_viral'] == 1 and row['spotify_dominant'] ==1:
        return 'Both Platforms'
    elif row['tiktok_viral'] ==1 and row['spotify_dominant'] ==0:
        return 'TikTok Only'
    elif row['tiktok_viral'] ==0 and row['spotify_dominant'] ==1:
        return 'Spotify Only' 
    else:
        return 'Neither'
    

df_spotify['platform_category'] = df_spotify.apply(categorize, axis=1)

# Pie chart
st.subheader("Platform Dominance Breakdown")
fig, ax =plt.subplots()
category_counts= df_spotify['platform_category'].value_counts()
ax.pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%', colors=['grey', 'red', 'blue', 'green'])
ax.set_title('Song Performance: TikTok vs Spotify')
st.pyplot(fig)

# Bar Chart Comparison
st.subheader("Average Metrics by Platform Category")
fig2, axes= plt.subplots(1, 3, figsize=(15, 5))

metrics=['Spotify Popularity', 'TikTok Views', 'Spotify Streams']
colors = ['blue', 'red', 'green']

for ax, metric, color in zip(axes, metrics, colors):
    data=df_spotify.groupby('platform_category')[metric].mean()
    ax.bar(data.index, data.values, color=color, alpha=0.7)
    ax.set_title(metric)
    ax.set_ylabel('Average Value')
    ax.tick_params(axis='x', rotation=45)


plt.tight_layout()
st.pyplot(fig2)

# Key findings
st.subheader("Key Findings")
st.write("**1.** TikTok virality and Spotify dominance are largely independent — only 10.0% of songs crack both platforms")
st.write("**2.** TikTok Only songs average 3.6 billion views but only 254M Spotify streams")
st.write("**3.** Spotify Only songs have higher popularity scores (70) despite low TikTok presence")
st.write("**4.** Loudness and tempo are the strongest audio predictors of popularity")

# Song search 
st.subheader("Search a Song")
search=st.text_input("Type a song or artist name:")

if search:
    results=df_spotify[
        df_spotify['Track'].str.contains(search, case=False, na=False) |
        df_spotify['Artist'].str.contains(search, case=False, na=False)

    ][['Track', 'Artist', 'platform_category', 'Spotify Streams', 'TikTok Views']]

    if len(results) ==0:
        st.write("No songs found. Try a different name.")
    else:
        st.dataframe(results, hide_index=True)

# Scatter plot
st.subheader("TikTok Views vs Spotify Streams")
fig3, ax=plt.subplots(figsize=(10,6))
colors_map={
    'Both Platforms': 'green',
    'TikTok Only': 'red',
    'Spotify Only': 'blue',
    'Neither': 'grey'
}

for category, group in df_spotify.groupby('platform_category'):
    ax.scatter(
        group['TikTok Views'],
        group['Spotify Streams'],
        c=colors_map[category],
        label=category,
        alpha=0.5,
        s=20
)

ax.set_xlabel('TikTok Views')
ax.set_ylabel('Spotify Streams')
ax.set_title('TikTOk Views vs Spotify Streams by Platform Category')
ax.legend()
plt.tight_layout()
st.pyplot(fig3)

# Top 10 songs per category
st.subheader("Top Songs by Category")

category_choice=st.selectbox(
    "Select a category:",
    ['Both Platforms', 'TikTok Only', 'Spotify Only', 'Neither']
)

if category_choice =='TikTok Only':
    top10=df_spotify[df_spotify['platform_category']==category_choice].nlargest(10, 'TikTok Views')[['Track', 'Artist', 'TikTok Views', 'Spotify Streams']]
elif category_choice == 'Both Platforms':
    top10=df_spotify[df_spotify['platform_category'] == category_choice].nlargest(10, 'combined_score')[['Track', 'Artist', 'TikTok Views', 'Spotify Streams']]
else:
    top10=df_spotify[df_spotify['platform_category']== category_choice].nlargest(10, 'Spotify Streams')[['Track', 'Artist', 'TikTok Views', 'Spotify Streams']]

top10=top10.reset_index(drop=True)
top10.index=top10.index+1
top10.index.name='Rank'
top10['TikTok Views'] = top10['TikTok Views'].apply(lambda x: f"{x:,.0f}")
top10['Spotify Streams'] = top10['Spotify Streams'].apply(lambda x: f"{x:,.0f}")
st.dataframe(top10)

st.subheader("What Makes a Both Platforms Hit?")
st.write("Songs that dominate both platforms average **73 Spotify popularity** and **3 billion TikTok views** — significantly higher than any other category.")
st.write("Only **10% of songs** crack both platforms, suggesting that true cross-platform success is rare and requires both strong audio quality AND viral potential.")
st.write("Examples: Blinding Lights, Shape of You, As It Was — songs with massive mainstream appeal that translate across different listening behaviors.")
st.caption("Both Platforms ranking uses a combined score: normalized TikTok Views + normalized Spotify Streams. This rewards songs that perform strongly on both platforms equally.")

# ML Model Results
st.subheader("Machine Learning: Can We Predict a Hit?")
st.write("We trained 3 models to predict whether a TikTok trending song would be a Spotify hit based on audio features alone.")

# Model Results
model_results=pd.DataFrame({
    'Model' : ['Random Forest', 'Graident Boosting', 'Logistic Regression'],
    'Accuracy': ['60.1%', '60.0%', '59.4%']
})

st.dataframe(model_results, hide_index=True)

st.write("**Key Finding:** All three models converged around 60% accuracy — only slightly better than random guessing (50%). This suggests that audio features alone cannot predict virality.")
st.write("**Why?** Factors like artist following, release timing, social trends, and playlist placement likely play a bigger role than the sound of the song itself.")
st.write("**Top predictive features:** Loudness, Tempo, and Valence were the strongest audio predictors — but even combined, they couldn't push accuracy above 60%.")


    
