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

proyecto-algebra-relacional/
├── docker-compose.yml      # Orquestador de servicios (App + DB)
├── README.md               # Documentación principal
├── app/
│   ├── Dockerfile          # Configuración de imagen Python
│   ├── main.py             # Código fuente del Menú Interactivo
│   └── requirements.txt    # Dependencias (psycopg2, tabulate)
└── db/
    └── init.sql            # Script SQL: Creación de tablas y datos semilla
