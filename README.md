# Pocket Goodreads Data Service

Cong cu crawl quotes tu Goodreads theo danh sach tag cau hinh san va luu ket qua ra file CSV.

## Chuc nang

- Crawl quotes theo cac tag Goodreads trong `URLS`.
- Ho tro crawl nhieu page qua `START_PAGE` va `END_PAGE`.
- Tach text lay duoc tu `QUOTE_XPATH` thanh quote, author, va book.
- Bo qua quote trung lap trong tung tag.
- Luu CSV vao thu muc `data` nam cung thu muc voi source code.

## Yeu cau

- Python 3.9 tro len.
- Script chay se tu tao virtual environment rieng trong `.venv`.
- Thu vien can thiet duoc khai bao trong `requirements.txt` va duoc cai tu dong.

## Cach chay tren macOS

Cap quyen chay cho script lan dau:

```bash
chmod +x run_goodreads_crawl.sh
```

Chay crawler:

```bash
./run_goodreads_crawl.sh
```

Script se tu tao `.venv`, cai dependencies, sau do chay crawler bang Python trong env nay.

## Cach chay tren Windows

Mo file:

```bat
run_goodreads_crawl.bat
```

Hoac chay truc tiep:

```bat
python goodreads_quotes_crawl.py
```

Khuyen nghi dung file `.bat` de script tu tao `.venv` va cai dependencies truoc khi chay.

## Cau hinh crawl

Mo `goodreads_quotes_crawl.py` va sua cac bien sau:

- `URLS`: danh sach URL/tag Goodreads can crawl.
- `START_PAGE`: page bat dau.
- `END_PAGE`: page ket thuc.

Vi du:

```python
START_PAGE = 1
END_PAGE = 5
```

## Du lieu dau ra

Crawler tu tao thu muc `data` neu chua ton tai. Moi tag se duoc luu thanh mot file CSV rieng:

```text
data/life.csv
data/success.csv
data/love.csv
```

Moi file CSV co cac cot:

- `id`
- `quote`
- `author`
- `book`

## Ghi chu

- File CSV duoc ghi voi encoding `utf-8-sig` de mo tot tren Excel.
- Neu mot page loi, script se in log loi va tiep tuc voi page/tag tiep theo.
- Text crawl duoc trim whitespace, xoa quote marks, tach quote/author bang dash, va tach author/book bang dau phay dau tien.
