# 🚀 Data Journey Challenge – Technical Test

This project was developed as part of a **technical assessment** for a **Data/Analytics Engineer** position.  
The goal is to **ingest, validate, transform, and generate reports** from an employee dataset.

---

## 📂 Project Structure

```
.
├── data/
│ └── funcionarios.csv
├── output/
│ ├── erros.csv 
│ ├── relatorio_individual.csv
│ └── kpis.json 
├── src/
│ ├── reader.py 
│ ├── schema.py
│ ├── transform.py 
│ └── kpis.py 
├── main.py 
├── pyproject.toml
└── README.md 
```


## 🎯 Objective

Starting from the file `funcionarios.csv`, the pipeline must:

1. **Validate data:**
   - Name cannot be empty or contain numbers.  
   - Area must be one of: `Vendas`, `TI`, `Financeiro`, `RH`, `Operações`.  
   - Salary must be ≥ 0.  
   - Bonus percentage must be between 0 and 1.

2. **Calculate the final bonus:**
   ```python
   BONUS_BASE = 1000
   bonus_final = BONUS_BASE + salario * bonus_percentual

3. **Generate reports:**

   - relatorio_individual.csv → valid records + bonus_final.

   - erros.csv → invalid records.

   - kpis.json → aggregated indicators:

   - Number of employees per area

   - Average salary per area

   - Total bonus sum

   - Top 3 employees with highest bonus*

##  🧰 Tech Stack

   -  Python 3.10+

   -  Pandas

   -  Pandera — for schema validation

   -  JSON — for KPI export