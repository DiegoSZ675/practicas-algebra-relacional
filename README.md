# TechStore - Sistema de Gestión con Álgebra Relacional y SQL 🛒

Este proyecto implementa un sistema de base de datos para una tienda de electrónica ("TechStore"), demostrando la equivalencia y aplicación práctica de **Álgebra Relacional**, **Cálculo Relacional** y **SQL Estándar**.

El sistema está completamente dockerizado e incluye un menú interactivo en Python para ejecutar y visualizar 20 consultas complejas.

**Integrantes del Equipo:**
* [Tu Nombre Completo Aquí]
* [Nombre de tu compañero (si aplica)]

---

## 📋 Descripción del Dominio

El proyecto modela el flujo operativo de una tienda en línea especializada en tecnología, gestionando:
* **Inventario:** Productos clasificados por categorías con control de stock.
* **Ventas:** Pedidos realizados por clientes, con seguimiento de estados y métodos de pago.
* **Clientes:** Información de contacto y ubicación para envíos.
* **Detalle de Compras:** Relación detallada de productos por pedido (cantidad, precio unitario).

### Modelo Relacional (Esquema)
1. **CATEGORIAS** (`id_cat` PK, `nombre`, `descripcion`, `iva_porcentaje`)
2. **PRODUCTOS** (`id_prod` PK, `nombre`, `marca`, `precio`, `stock`, `id_cat` FK)
3. **CLIENTES** (`id_cli` PK, `nombre`, `apellido`, `email`, `ciudad`, `telefono`)
4. **PEDIDOS** (`id_ped` PK, `fecha`, `estado`, `metodo_pago`, `total`, `id_cli` FK)
5. **DETALLES** (`id_ped` FK, `id_prod` FK, `cantidad`, `precio_unitario`, `descuento`)

---

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
        string id_ped PK
        string id_prod PK
        int quantity
    }
```

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
## 🚀 Instalación y Ejecución
```text
Este proyecto utiliza Docker y Docker Compose para un despliegue inmediato y aislado. No requiere instalar PostgreSQL ni Python localmente.

Prerrequisitos
Tener instalado Docker Desktop (o Docker Engine + Compose).

Pasos para ejecutar
1. Clonar el repositorio:
git clone <URL_DE_TU_REPOSITORIO>
cd proyecto-algebra-relacional
2. Construir y levantar los contenedores: Este comando descarga la imagen de Postgres, construye la aplicación Python e inicializa la base de datos automáticamente.
3. Ingresar al Menú Interactivo: Una vez que los contenedores estén corriendo, ejecuta:
docker attach techstore_menu
(Nota: Si el menú no aparece de inmediato, presiona ENTER una vez).

4. Detener el sistema: Para apagar los contenedores y liberar recursos:
docker-compose down
```
##🧠 Consultas Implementadas
```text
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
