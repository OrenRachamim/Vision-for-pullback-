# Vision for pullback

* `pullback_scanner.py` - הסורק המתוקן: זיהוי ירידה > האטה > בסיס > פריצה, בגרף יומי ושבועי
  (שיא אמיתי, ירידה עד השפל האמיתי, הגדרה חדשה לשלב ההאטה. פירוט ב-`ANALYSIS.md` סעיף 6).
* `pullback_scanner_v1.py` - הסורק המקורי, ללא שינוי, להשוואה.
* `backtest.py` - מנוע walk-forward שמריץ את הסורק על היסטוריה אמיתית, יום אחרי יום בלי הצצה לעתיד,
  ומודד מה קרה אחרי כל איתות מול קבוצות השוואה.
* `find_buy_signals.py` - מוצא איתותים משולבים (שבועי דורך, ואחריו יומי מפעיל) ומצייר גרף יומי + שבועי לכל אחד.
* `ANALYSIS.md` - ניתוח הקוד ותוצאות הריצה. **מומלץ להתחיל כאן.**

## התקנה והרצה (Windows / Mac / Linux)

```bash
pip install -r requirements.txt

python pullback_scanner.py AAPL MSFT          # הסורק עצמו, היום
python backtest.py                            # 30 מניות ברירת מחדל, 2016 עד היום (~1-2 דקות)
python backtest.py AAPL NVDA AMD --start 2019-01-01 --charts 30
python backtest.py --target-r 3 --max-hold 40 # כללי יציאה אחרים
python backtest.py --csv-dir my_data SPY      # נתונים משלך: my_data/SPY.csv עם Date,Open,High,Low,Close,Volume
python backtest.py --scanner pullback_scanner_v1 --out results_v1   # הגרסה המקורית
python backtest.py --universe universes/sp500.txt universes/sp400.txt --weekly-only   # ~900 מניות, שבועי בלבד
python backtest.py --universe universes/sp500.txt universes/sp400.txt --combo --max-hold 10   # איתות משולב
python find_buy_signals.py --universe universes/sp500.txt --max 10   # איתותים משולבים אחרונים, עם גרפים
python backtest.py --universe universes/sp500.txt universes/sp400.txt --index-combo market --trail-atr 3 --max-hold 60   # מניה + מדד
python index_control.py results --universe universes/sp500.txt --index-combo market --trail-atr 3 --max-hold 60   # בדיקות חוסן
python -m pytest -q tests                     # בדיקות תקינות למנוע
```

נתונים מורדים פעם אחת ל-`data/` (מטמון). `--refresh` מוריד מחדש.

## תוצרים (`results/` לגרסה המתוקנת, `results_v1/` למקורית)

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
| `--universe` | - | קובץ/קבצים עם טיקר בכל שורה (יש `universes/sp500.txt`, `sp400.txt`) |
| `--combo` | כבוי | איתות משולב: שבועי דורך, יומי באותו יום או אחריו מפעיל קנייה |
| `--arm-days` | 15 | כמה ימי מסחר אחרי השבועי איתות יומי עדיין נחשב |
| `--index-combo` | - | `market` (SPY/MDY/IJR) או `sector` (XLK/XLF/...): קנייה כשגם המניה וגם המדד שלה באיתות פולבק יומי |
| `--index-window` | 5 | כמה ימי מסחר לפני איתות המניה איתות המדד עדיין נחשב |
| `--trail-atr` | - | סטופ נגרר: הגבוה מאז הכניסה פחות K×ATR14, בלי יעד קבוע |
| `--require-uptrend` | כבוי | במשולב: הקנייה רק מעל SMA200 (וה-CONTROL בהתאם) |
| `--weekly-only` | כבוי | רק הזיהוי השבועי, הרבה יותר מהיר ליוניברס גדול |
| `--scanner` | pullback_scanner | איזו גרסה לבדוק |
| `--jobs` | מספר ליבות | עיבוד מקבילי |

הערות: מחירי yfinance מותאמים לדיבידנדים ולפיצולים; רשימת מניות של היום יוצרת הטיית שרידות (survivorship bias).
