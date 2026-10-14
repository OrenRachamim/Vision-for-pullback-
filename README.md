# Vision for pullback

* `pullback_scanner.py` - הסורק המקורי (ללא שינוי): זיהוי ירידה > האטה > בסיס > פריצה, בגרף יומי ושבועי.
* `backtest.py` - מנוע walk-forward שמריץ את הסורק על היסטוריה אמיתית, יום אחרי יום בלי הצצה לעתיד,
  ומודד מה קרה אחרי כל איתות מול קבוצות השוואה.
* `ANALYSIS.md` - ניתוח הקוד ותוצאות הריצה. **מומלץ להתחיל כאן.**

## התקנה והרצה (Windows / Mac / Linux)

```bash
pip install -r requirements.txt

python pullback_scanner.py AAPL MSFT          # הסורק עצמו, היום
python backtest.py                            # 30 מניות ברירת מחדל, 2016 עד היום (~1-2 דקות)
python backtest.py AAPL NVDA AMD --start 2019-01-01 --charts 30
python backtest.py --target-r 3 --max-hold 40 # כללי יציאה אחרים
python backtest.py --csv-dir my_data SPY      # נתונים משלך: my_data/SPY.csv עם Date,Open,High,Low,Close,Volume
python -m pytest -q tests                     # בדיקות תקינות למנוע
```

נתונים מורדים פעם אחת ל-`data/` (מטמון). `--refresh` מוריד מחדש.

## תוצרים (`results/`)

| קובץ | תוכן |
|---|---|
| `summary.md` | טבלאות: תשואה קדימה מול baseline, סימולציית עסקאות מול CONTROL, פילוח לפי score / רכיב / שנה / מניה |
| `signals.csv` | שורה לכל איתות: תאריך, score, רכיבים, אורכי שלבים, רמות, תשואות קדימה, תוצאת עסקה |
| `equity.png` | R מצטבר לאורך זמן |
| `charts/` | גרף הסורק עצמו ביום האיתות + 20 נרות אחריו (שם הקובץ כולל את תוצאת העסקה) |

## אפשרויות

| דגל | ברירת מחדל | |
|---|---|---|
| `--start`, `--end` | 2016-01-01, היום | תקופת הבדיקה |
| `--target-r` | 2 | יעד רווח בכפולות הסיכון (כניסה - base_lo) |
| `--max-hold` | 20 | יציאה בזמן (ימי מסחר) |
| `--cooldown` | 5 | איתות חוזר על אותה מניה תוך N נרות נספר פעם אחת |
| `--charts` | 12 | כמה גרפי איתות לצייר (מדגם אקראי קבוע) |
| `--no-prefilter` | כבוי | ריצה איטית בלי סינון מוקדם, לאימות |
| `--jobs` | מספר ליבות | עיבוד מקבילי |

הערות: מחירי yfinance מותאמים לדיבידנדים ולפיצולים; רשימת מניות של היום יוצרת הטיית שרידות (survivorship bias).
