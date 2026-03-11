

# import sys, json, pandas as pd
#
# title = sys.argv[1].lower()
#
# df = pd.read_csv("books_latest.csv")
#
# match = df[df["title"].str.lower().str.contains(title, na=False)]
#
# if match.empty:
#     print("{}")
# else:
#     row = match.iloc[0]
#     print(json.dumps({
#         "bookId": str(row["bookId"]),
#         "title": row["title"],
#         "author": row.get("author", "")
#     }, ensure_ascii=False))


import sys, json, pandas as pd, os

query = sys.argv[1].lower()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "books_latest.csv")

df = pd.read_csv(CSV_PATH, encoding="utf-8")

matches = df[df["title"].str.lower().str.contains(query, na=False)]

# lấy 5 sách đầu tiên
matches = matches.head(5)

# nếu không có gì thì trả object rỗng
if matches.empty:
    print("[]")
else:
    suggestions = []
    for _, row in matches.iterrows():
        suggestions.append({
            "bookId": str(row["bookId"]),
            "title": row["title"],
            "author": row.get("author", "")
        })
    print(json.dumps(suggestions, ensure_ascii=False))
