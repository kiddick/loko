## LOKO project

unpack archive `unzip loko-master.zip`

```bash
cd loko-master

python -m venv ./.venv/loko
. .venv/loko/bin/activate
pip install -r requirements.txt

touch loko/db.sqlite3
python manage.py migrate

python manage.py importdata test_LT.xlsx

python manage.py runserver
```
Now you could open http://localhost:8000/ and check data and charts

By default empty filter queries all branches with all train series