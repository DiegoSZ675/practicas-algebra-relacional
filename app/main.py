import os
import time
import psycopg2
from tabulate import tabulate

def get_db_connection():
    while True:
        try:
            conn = psycopg2.connect(
                host=os.environ['DB_HOST'],
                database=os.environ['DB_NAME'],
                user=os.environ['DB_USER'],
                password=os.environ['DB_PASS']
            )
            return conn
        except psycopg2.OperationalError:
            print("Esperando a la base de datos...")
            time.sleep(2)

# === DICCIONARIO DE CONSULTAS (LAS 20 COMPLETAS) ===
consultas = {
    # --- GRUPO 1: OPERADORES BÁSICOS (5) ---
    "1": {
        "cat": "Básicas",
        "titulo": "Selección Simple",
        "desc": "Productos de la marca Apple",
        "algebra": "σ (marca='Apple') (PRODUCTOS)",
        "calculo": "{t | PRODUCTOS(t) ∧ t.marca='Apple'}",
        "sql": "SELECT * FROM PRODUCTOS WHERE marca = 'Apple';"
    },
    "2": {
        "cat": "Básicas",
        "titulo": "Selección con Rango",
        "desc": "Pedidos con total entre 500 y 1000",
        "algebra": "σ (total ≥ 500 ∧ total ≤ 1000) (PEDIDOS)",
        "calculo": "{t | PEDIDOS(t) ∧ t.total ≥ 500 ∧ t.total ≤ 1000}",
        "sql": "SELECT * FROM PEDIDOS WHERE total BETWEEN 500 AND 1000;"
    },
    "3": {
        "cat": "Básicas",
        "titulo": "Proyección Simple",
        "desc": "Listar solo nombres y emails de clientes",
        "algebra": "π nombre, email (CLIENTES)",
        "calculo": "{t.nombre, t.email | CLIENTES(t)}",
        "sql": "SELECT nombre, email FROM CLIENTES;"
    },
    "4": {
        "cat": "Básicas",
        "titulo": "Unión de Conjuntos",
        "desc": "Productos Apple UNIDO a productos Samsung",
        "algebra": "σ(marca='Apple') ∪ σ(marca='Samsung')",
        "calculo": "{t | PRODUCTOS(t) ∧ (t.marca='Apple' ∨ t.marca='Samsung')}",
        "sql": "SELECT * FROM PRODUCTOS WHERE marca = 'Apple' UNION SELECT * FROM PRODUCTOS WHERE marca = 'Samsung';"
    },
    "5": {
        "cat": "Básicas",
        "titulo": "Diferencia de Conjuntos",
        "desc": "Categorías que NO tienen productos asignados (simulado)",
        "algebra": "π id_cat (CATEGORIAS) - π id_cat (PRODUCTOS)",
        "calculo": "{c.id_cat | CATEGORIAS(c) ∧ ¬∃p(PRODUCTOS(p) ∧ p.id_cat=c.id_cat)}",
        "sql": "SELECT id_cat FROM CATEGORIAS EXCEPT SELECT id_cat FROM PRODUCTOS;"
    },

    # --- GRUPO 2: REUNIONES / JOINS (5) ---
    "6": {
        "cat": "Joins",
        "titulo": "Reunión Natural",
        "desc": "Nombre de productos y sus categorías",
        "algebra": "PRODUCTOS ⋈ CATEGORIAS",
        "calculo": "{p.nombre, c.nombre | PRODUCTOS(p) ∧ CATEGORIAS(c) ∧ p.id_cat=c.id_cat}",
        "sql": "SELECT P.nombre, C.nombre as categoria FROM PRODUCTOS P JOIN CATEGORIAS C ON P.id_cat = C.id_cat;"
    },
    "7": {
        "cat": "Joins",
        "titulo": "Reunión de 3 Tablas",
        "desc": "Cliente -> Pedido -> Detalle (Quién compró qué)",
        "algebra": "CLIENTES ⋈ PEDIDOS ⋈ DETALLES",
        "calculo": "Join complejo con existenciales",
        "sql": """
            SELECT C.nombre, P.id_ped, D.id_prod 
            FROM CLIENTES C 
            JOIN PEDIDOS P ON C.id_cli = P.id_cli
            JOIN DETALLES D ON P.id_ped = D.id_ped;
        """
    },
    "8": {
        "cat": "Joins",
        "titulo": "Left Outer Join",
        "desc": "Clientes y sus pedidos (incluso si no tienen)",
        "algebra": "CLIENTES ⟕ PEDIDOS",
        "calculo": "No soportado nativamente en CRT básico",
        "sql": "SELECT C.nombre, P.id_ped FROM CLIENTES C LEFT JOIN PEDIDOS P ON C.id_cli = P.id_cli;"
    },
    "9": {
        "cat": "Joins",
        "titulo": "Anti-Join",
        "desc": "Clientes que NUNCA han comprado",
        "algebra": "CLIENTES ▷ PEDIDOS",
        "calculo": "{c | CLIENTES(c) ∧ ¬∃p(PEDIDOS(p) ∧ p.id_cli=c.id_cli)}",
        "sql": "SELECT * FROM CLIENTES C WHERE NOT EXISTS (SELECT 1 FROM PEDIDOS P WHERE P.id_cli = C.id_cli);"
    },
    "10": {
        "cat": "Joins",
        "titulo": "Self Join",
        "desc": "Pares de productos diferentes con el mismo precio",
        "algebra": "ρ(P1, PROD) ⋈ ρ(P2, PROD)",
        "calculo": "{p1, p2 | PROD(p1) ∧ PROD(p2) ∧ p1.precio=p2.precio ∧ p1.id != p2.id}",
        "sql": """
            SELECT P1.nombre, P2.nombre, P1.precio 
            FROM PRODUCTOS P1 JOIN PRODUCTOS P2 
            ON P1.precio = P2.precio AND P1.id_prod < P2.id_prod;
        """
    },

    # --- GRUPO 3: AGREGACIÓN Y AGRUPACIÓN (5) ---
    "11": {
        "cat": "Agregación",
        "titulo": "Función Agregada Simple",
        "desc": "Precio promedio de todos los productos",
        "algebra": "F avg(precio) (PRODUCTOS)",
        "calculo": "No aplica estándar",
        "sql": "SELECT ROUND(AVG(precio), 2) as promedio_global FROM PRODUCTOS;"
    },
    "12": {
        "cat": "Agregación",
        "titulo": "Agrupación Simple",
        "desc": "Cantidad de productos por categoría",
        "algebra": "γ id_cat; COUNT(id_prod) (PRODUCTOS)",
        "calculo": "No aplica estándar",
        "sql": "SELECT id_cat, COUNT(*) as cantidad FROM PRODUCTOS GROUP BY id_cat;"
    },
    "13": {
        "cat": "Agregación",
        "titulo": "Agrupación con SUM",
        "desc": "Total gastado por cada cliente (Histórico)",
        "algebra": "γ id_cli; SUM(total) (PEDIDOS)",
        "calculo": "No aplica estándar",
        "sql": "SELECT id_cli, SUM(total) as gasto_total FROM PEDIDOS GROUP BY id_cli;"
    },
    "14": {
        "cat": "Agregación",
        "titulo": "Agrupación con HAVING",
        "desc": "Marcas con precio promedio mayor a 500",
        "algebra": "σ prom>500 (γ marca; AVG(precio)->prom (PRODUCTOS))",
        "calculo": "No aplica estándar",
        "sql": "SELECT marca, AVG(precio) FROM PRODUCTOS GROUP BY marca HAVING AVG(precio) > 500;"
    },
    "15": {
        "cat": "Agregación",
        "titulo": "Agregación Compleja",
        "desc": "Total de inventario valorizado (Precio * Stock)",
        "algebra": "F sum(val) (π precio*stock->val (PRODUCTOS))",
        "calculo": "No aplica estándar",
        "sql": "SELECT SUM(precio * stock) as valor_inventario FROM PRODUCTOS;"
    },

    # --- GRUPO 4: DIVISIÓN RELACIONAL (3) ---
    "16": {
        "cat": "División",
        "titulo": "División Exacta",
        "desc": "Clientes que compraron TODOS los productos de C3 (Tablets)",
        "algebra": "COMPRAS ÷ PRODUCTOS(C3)",
        "calculo": "∀p (p ∈ C3 → ∃compra)",
        "sql": """
            SELECT C.nombre FROM CLIENTES C
            WHERE NOT EXISTS (
                SELECT id_prod FROM PRODUCTOS WHERE id_cat = 'C3'
                EXCEPT
                SELECT D.id_prod FROM DETALLES D 
                JOIN PEDIDOS P ON D.id_ped = P.id_ped 
                WHERE P.id_cli = C.id_cli
            );
        """
    },
    "17": {
        "cat": "División",
        "titulo": "División por Ciudad",
        "desc": "Ciudades donde se han vendido TODOS los tipos de Laptops",
        "algebra": "VENTAS_CIUDAD ÷ LAPTOPS",
        "calculo": "∀l (l ∈ Laptop → ∃venta_ciudad)",
        "sql": """
            SELECT DISTINCT C.ciudad FROM CLIENTES C
            WHERE NOT EXISTS (
                SELECT id_prod FROM PRODUCTOS WHERE id_cat = 'C1'
                EXCEPT
                SELECT D.id_prod FROM DETALLES D
                JOIN PEDIDOS P ON D.id_ped = P.id_ped
                JOIN CLIENTES CL ON P.id_cli = CL.id_cli
                WHERE CL.ciudad = C.ciudad
            );
        """
    },
    "18": {
        "cat": "División",
        "titulo": "División Estricta",
        "desc": "Pedidos que contienen TODOS los productos de Apple (Difícil)",
        "algebra": "DETALLES_PED ÷ PROD_APPLE",
        "calculo": "∀p (p ∈ Apple → p ∈ Detalle_Pedido)",
        "sql": """
            SELECT id_ped FROM PEDIDOS P
            WHERE NOT EXISTS (
                SELECT id_prod FROM PRODUCTOS WHERE marca = 'Apple'
                EXCEPT
                SELECT id_prod FROM DETALLES D WHERE D.id_ped = P.id_ped
            );
        """
    },

    # --- GRUPO 5: CUANTIFICADORES UNIVERSALES / LOGICA (2) ---
    "19": {
        "cat": "Lógica",
        "titulo": "Universal Implicación",
        "desc": "Categorías donde TODOS sus productos tienen stock > 0",
        "algebra": "Lógica universal traducida a NOT EXISTS",
        "calculo": "∀p (p ∈ Cat → p.stock > 0)",
        "sql": """
            SELECT C.nombre FROM CATEGORIAS C
            WHERE NOT EXISTS (
                SELECT 1 FROM PRODUCTOS P 
                WHERE P.id_cat = C.id_cat AND P.stock <= 0
            );
        """
    },
    "20": {
        "cat": "Lógica",
        "titulo": "Doble Negación",
        "desc": "Clientes que NO tienen pedidos CANCELADOS",
        "algebra": "CLIENTES - (CLIENTES ⋈ σ estado='Cancelado' PED)",
        "calculo": "¬∃p (PEDIDO(p) ∧ p.estado='Cancelado')",
        "sql": """
            SELECT nombre FROM CLIENTES
            WHERE id_cli NOT IN (
                SELECT id_cli FROM PEDIDOS WHERE estado = 'Cancelado'
            );
        """
    }
}

def menu():
    conn = get_db_connection()
    cur = conn.cursor()

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== TECHSTORE: SISTEMA ALGEBRA RELACIONAL ===")
        print(f"{'ID':<4} {'CATEGORÍA':<12} {'CONSULTA'}")
        print("-" * 50)
        
        for key, val in consultas.items():
            print(f"{key:<4} {val['cat']:<12} {val['titulo']}")
        
        print("\nX. Salir")
        
        opcion = input("\nSeleccione ID de consulta: ").upper()
        
        if opcion == 'X':
            break
            
        if opcion in consultas:
            q = consultas[opcion]
            print(f"\n>>> {q['titulo']} <<<")
            print(f"Descripción: {q['desc']}")
            print(f"Álgebra Rel.: {q['algebra']}")
            print(f"Cálculo Rel.: {q['calculo']}")
            print(f"\nSQL Ejecutado:\n{q['sql']}")
            print("\nRESULTADO:")
            
            try:
                cur.execute(q['sql'])
                rows = cur.fetchall()
                if rows:
                    colnames = [desc[0] for desc in cur.description]
                    print(tabulate(rows, headers=colnames, tablefmt="grid"))
                else:
                    print("--> La consulta no devolvió resultados (Conjunto Vacío).")
            except Exception as e:
                print(f"Error SQL: {e}")
                conn.rollback()
            
            input("\nPresione ENTER para volver al menú...")

    cur.close()
    conn.close()

if __name__ == '__main__':
    menu()
