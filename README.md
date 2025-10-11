# Acelerador - Jornada de Dados – Technical Test

The goal of this project is to implement a Data Engineering pipeline that ingests employee data, applies rigorous validation (Schema Validation), and generates analytical reports and performance metrics (KPIs).


---

## 📂 Project Structure

```
.
├── data/
│ └── funcionarios.csv
├── logs/
│ └── etl_{date}_{hour}.log
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

## Objective and Pipeline Flow

The pipeline starts by reading `funcionarios.csv` and follows these steps:


### 1. ⚙️ Transformação & Validação (T)

Data is validated row-by-row using Pandera before any calculations occur.


| Field | Validation Rule |
| :--- | :--- |
| **name** | Cannot be empty or contain numbers. |
| **area** | Must be one of: Vendas, TI, Financeiro, RH, Operações. |
| **salary** | Must be a number greater than or equal to 0. |
| **percentual_bonus** | Must be a number between 0 and 1 (inclusive). |

**Bonus Calculation:** The `bonus_final` is calculated only for records that pass validation:

$$
\text{bonus\_final} = 1000 + \text{salario} \times \text{bonus\_percentual}
$$

### 2. Reports and KPIs (L)

| Arquivo de Saída | Conteúdo | Logs de Êxito |
| :--- | :--- | :--- |
| **relatorio_individual.csv** | All valid records, including the calculated bonus_final. | Yes (path and lines written) |
| **erros.csv** | 	All records that failed validation, with the reason for the error appended. | Yes (path and lines written) |
| **kpis.json** | Aggregated metrics, including: Count by Area, Average Salary by Area, Total Bonus Sum, and Top 3 employees with the highest bonus. | Yes (Top 3 summary and file path) |

---

## Observability: Structured Logging with loguru

The pipeline uses the **`loguru`** library to ensure traceability and simplify debugging.

* **Centralized Configuration:**  `main.py` configures logs for the console and a dedicated file (`logs/etl_{date}_{time}.log`).

* **Real-Time Metrics:** Logs record crucial metrics at each stage:
    * **Extract:**  Count of lines read.
    * **Transform:**  Proportion of valid vs. invalid records and the Top 3 reasons for errors.
    * **Load:**  Files generated, paths, and lines written per report.


---

## 🧰 Tech Stack & Requisitos

| Technology | Purpose |
| :--- | :--- |
| **Python 3.10+** | Primary development language. |
| **Pandas** | DataFrame manipulation and data aggregation. |
| **Pandera** | Rigorous Schema Validation and error collection |
| **Loguru** | Structured logging, observability, and metric recording. |
| **JSON** | Exporting the final KPI file. |

### Instalação e Execução (Usando Poetry)

1.  Clone the repository.


2.  Install dependencies:
    ```bash
    poetry install
    ```
3.  Execute the pipeline:
    ```bash
    poetry run python main.py
    ```