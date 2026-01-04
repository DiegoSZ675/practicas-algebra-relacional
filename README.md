## 📊 Diagrama del Esquema (EER)

```mermaid
erDiagram
    CATEGORIAS ||--|{ PRODUCTOS : contiene
    PRODUCTOS ||--o{ DETALLES : incluido_en
    PEDIDOS ||--|{ DETALLES : tiene
    CLIENTES ||--o{ PEDIDOS : realiza

    CATEGORIAS {
        string id_cat PK
        string nombre
        decimal iva
    }
    PRODUCTOS {
        string id_prod PK
        string nombre
        decimal precio
        string id_cat FK
    }
    CLIENTES {
        string id_cli PK
        string email
        string ciudad
    }
    PEDIDOS {
        string id_ped PK
        date fecha
        decimal total
        string id_cli FK
    }
    DETALLES {
        string id_ped PK, FK
        string id_prod PK, FK
        int quantity
    }

```
 Estructura del Proyecto


## 📂 Estructura del Repositorio

```text
proyecto-algebra-relacional/
├── docker-compose.yml      # Orquestador de servicios (App + DB)
├── README.md               # Documentación principal
├── app/
│   ├── Dockerfile          # Configuración de imagen Python
│   ├── main.py             # Código fuente del Menú Interactivo
│   └── requirements.txt    # Dependencias (psycopg2, tabulate)
└── db/
    └── init.sql            # Script SQL: Creación de tablas y datos semilla
```
## Tabla de equivalencias teóricas

```markdown
## 🎓 Equivalencias Teóricas

Este proyecto demuestra la traducción práctica de operadores matemáticos a SQL:

| Operador | Símbolo | Concepto | Implementación SQL |
| :--- | :---: | :--- | :--- |
| **Selección** | $\sigma$ | Filtrado de filas | `WHERE condicion` |
| **Proyección** | $\pi$ | Selección de columnas | `SELECT col1, col2` |
| **Reunión** | $\bowtie$ | Combinación de tablas | `JOIN ... ON ...` |
| **Agrupación** | $\gamma$ | Agrupar por atributo | `GROUP BY` |
| **División** | $\div$ | Totalidad ("Para todo") | `NOT EXISTS (EXCEPT)` |
| **Diferencia** | $-$ | Resta de conjuntos | `EXCEPT` o `NOT IN` |
```

