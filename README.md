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
