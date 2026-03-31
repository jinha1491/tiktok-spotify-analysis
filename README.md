# TikTok vs Spotify: What Makes a Song Go Viral?

A data science project analyzing 3,560 TikTok trending tracks and 4,370 top Spotify songs to uncover what drives virality across platforms.

 **[Live App](https://tiktok-spotify-jinha1491.streamlit.app)**

---

## Key Findings

- **TikTok and Spotify virality are largely independent** — only 10% of songs crack both platforms
- **TikTok Only songs average 3.6 billion views** but only 254M Spotify streams — viral TikTok songs don't convert to Spotify success
- **Spotify Only songs have higher popularity scores (70)** despite minimal TikTok presence
- **Audio features alone predict popularity with only 60% accuracy** — suggesting external factors like artist following, timing, and social trends matter more than sound

---

## Project Overview

### Data Sources
- **TikTok Trending Tracks** — 7,000 tracks with audio features (Kaggle)
- **Most Streamed Spotify Songs 2024** — 4,600 songs with cross-platform metrics (Kaggle)

### Analysis Pipeline
1. **Data Cleaning** — removed duplicates, handled missing values, converted numeric columns
2. **EDA** — audio feature distributions, correlation heatmap
3. **Platform Categorization** — classified songs into TikTok Only, Spotify Only, Both Platforms, Neither
4. **Machine Learning** — trained Random Forest, Gradient Boosting, and Logistic Regression classifiers
5. **Feature Importance** — identified loudness, tempo, and valence as top predictors
6. **Interactive App** — deployed Streamlit app with song search and visualizations

---

## Tech Stack

- **Python** — pandas, numpy, scikit-learn
- **Visualization** — matplotlib, seaborn
- **App** — Streamlit
- **Data** — Kaggle

---

## Run Locally
```bash
git clone https://github.com/jinha1491/tiktok-spotify-analysis.git
cd tiktok-spotify-analysis
pip install -r requirements.txt
streamlit run app.py
```

---

## Project Structure
```
tiktok-spotify-analysis/
├── app.py                          # Streamlit app
├── analysis.ipynb                  # Full analysis notebook
├── tiktok.csv                      # TikTok dataset
├── Most Streamed Spotify Songs 2024.csv  # Spotify dataset
└── requirements.txt                # Dependencies
```