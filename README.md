
# Stock Alert Bot – גרסה משודרגת

## איך להפעיל

### ניטור תיק אישי:
```bash
python main.py
```

### חיפוש מניות חמות מהשוק (Trending):
```bash
python explorer.py
```

### קבצים חשובים:
- explorer.py – סורק את השוק ומתריע על מניות שלא בתיק שלך
- core/trends.py – מאתר מניות חמות לפי טרנדים (Google/Fnviz)
- settings.py – כולל תקציב, מניות, גבולות
