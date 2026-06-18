# Agent Notes

## Muc tieu du an

Du an dung de crawl quotes tu Goodreads va xuat du lieu thanh CSV theo tung tag.

## File chinh

- `goodreads_quotes_crawl.py`: logic crawl, parse quote/author, va ghi CSV.
- `run_goodreads_crawl.bat`: script chay tren Windows.
- `run_goodreads_crawl.sh`: script chay tren macOS/Linux.
- `requirements.txt`: danh sach dependency duoc script cai vao `.venv`.
- `data/`: thu muc output CSV, duoc tao tu dong khi chay crawler.

## Nguyen tac khi chinh sua

- Giu code don gian, uu tien standard library neu co the.
- Khong hard-code duong dan tuyet doi cua may local.
- Script chay nen dung `.venv` rieng cua project va cai dependency tu `requirements.txt`.
- CSV phai duoc luu trong `data` cung thu muc voi source code.
- Neu them output crawl moi, dam bao `.gitignore` van khong commit file CSV sinh ra.
- Khi thay doi selector Goodreads, kiem tra lai `QUOTE_XPATH` va `AUTHOR_RELATIVE_XPATH`.

## Cach chay nhanh

macOS:

```bash
chmod +x run_goodreads_crawl.sh
./run_goodreads_crawl.sh
```

Windows:

```bat
run_goodreads_crawl.bat
```

## Kiem tra sau khi chay

- Thu muc `data` ton tai.
- Co file CSV theo tag, vi du `data/life.csv`.
- File CSV co header `id,quote,author`.
