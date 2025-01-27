# ds1 - Data Science learning form Belhard

# Home Work 3 (hw3.py) 
1. Выберите любой открытый датасет и скачайте открытый датасет, соответствующий вашим интересам или области обучения.
2. Создайте новую базу данных в системе управления базами данных (например, SQLite, PostgreSQL).
3. Создайте таблицу (или несколько таблиц) в базе данных с различными типами данных (INTEGER, TEXT, DATE), которые требуются для вашего датасета. Импортируйте данные из датасета в созданные таблицы.
4. Напишите несколько SQL-запросов для извлечения данных из таблиц базы данных. Используйте условия фильтрации (например, WHERE) для получения нужных данных.
5. Напишите SQL-запросы, использующие агрегатные функции (SUM, AVG, COUNT) для выполнения расчетов по данным таблицы.
6. Визуализируйте данные. Используйте библиотеки Python, такие как Matplotlib или Seaborn, для визуализации данных, извлеченных из базы данных. Постройте графики или диаграммы, которые помогут проанализировать и понять данные.

<h3>Power Consumption Prediction Dataset</h3>
<h5>Power consumption of three different distribution networks</h5>
This dataset is related to power consumption of three different distribution networks of Tetouan city which is located in north Morocco.

 - 0   DateTime               52416 non-null  object 
 - 1   Temperature            52416 non-null  float64
 - 2   Humidity               52416 non-null  float64
 - 3   Wind Speed             52416 non-null  float64
 - 4   general diffuse flows  52416 non-null  float64
 - 5   diffuse flows          52416 non-null  float64
 - 6   Zone 1                 52416 non-null  float64
 - 7   Zone 2                 52416 non-null  float64
 - 8   Zone 3                 52416 non-null  float64


# Home Work 2 (hw2.py)
1. Создайте модуль data_loader для загрузки данных из различных источников (CSV, JSON, API)
2. Создайте методы для добавления и удаления различных типов визуализации, таких как гистограммы, линейные графики и диаграммы рассеяния. Реализуйте эти методы. 
3. Создайте метод для подсчета пустых или пропущенных значений в каждом столбце DataFrame, а также метод для вывода отчета с информацией о пропущенных значениях. Реализуйте метод заполнения пропущенных значений (например: средним, медианой или наиболее частым значением).
4. Датасет выбрать самостоятельно исходя из интересов

<h3>Dataset on Anxiety Attacks</h3>
- ID
- Age  18 to 64
- Gender (Male, Female, Other)
- Occupation - Job role
- Sleep Hours - Daily sleep duration
- Physical Activity (hrs/week) (Exercise duration)
- Caffeine Intake (mg/day)
- Alcohol Consumption (drinks/week) drinks/week
- Smoking Yes/No
- Family History of Anxiety Yes/No

<h4>Модули</h4>
- hw2_modules/data_loader.py (класс загрузки датасета и получение его в формате DataFrame)
- hw2_modules/eda_analyze.py (класс для анализа, графического отображения, восстановления данных датасета)
 
<h4>Датасет</h4>
- anxiety_attack_data