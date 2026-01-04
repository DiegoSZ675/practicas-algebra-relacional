-- ==========================================
-- 1. LIMPIEZA INICIAL
-- ==========================================
DROP TABLE IF EXISTS RESENAS;
DROP TABLE IF EXISTS ENVIOS;
DROP TABLE IF EXISTS DETALLES;
DROP TABLE IF EXISTS PEDIDOS;
DROP TABLE IF EXISTS PRODUCTOS;
DROP TABLE IF EXISTS PROVEEDORES; -- Nueva
DROP TABLE IF EXISTS CLIENTES;
DROP TABLE IF EXISTS CATEGORIAS;

-- ==========================================
-- 2. CREACIÓN DE TABLAS (ESQUEMA DE 8 TABLAS)
-- ==========================================

-- Tabla 1: Categorías
CREATE TABLE CATEGORIAS (
    id_cat VARCHAR(10) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT,
    iva_porcentaje DECIMAL(5,2) DEFAULT 16.00
);

-- Tabla 2: Proveedores (NUEVA)
CREATE TABLE PROVEEDORES (
    id_prov VARCHAR(10) PRIMARY KEY,
    empresa VARCHAR(50),
    contacto VARCHAR(50),
    pais VARCHAR(30)
);

-- Tabla 3: Clientes
CREATE TABLE CLIENTES (
    id_cli VARCHAR(10) PRIMARY KEY,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    email VARCHAR(100),
    ciudad VARCHAR(50),
    telefono VARCHAR(20)
);

-- Tabla 4: Productos (Modificada para incluir Proveedor)
CREATE TABLE PRODUCTOS (
    id_prod VARCHAR(10) PRIMARY KEY,
    nombre VARCHAR(100),
    marca VARCHAR(50),
    precio DECIMAL(10,2),
    stock INT,
    id_cat VARCHAR(10),
    id_prov VARCHAR(10), -- Nuevo FK
    FOREIGN KEY (id_cat) REFERENCES CATEGORIAS(id_cat),
    FOREIGN KEY (id_prov) REFERENCES PROVEEDORES(id_prov)
);

-- Tabla 5: Pedidos
CREATE TABLE PEDIDOS (
    id_ped VARCHAR(10) PRIMARY KEY,
    fecha DATE,
    estado VARCHAR(20),
    metodo_pago VARCHAR(20),
    total DECIMAL(10,2),
    id_cli VARCHAR(10),
    FOREIGN KEY (id_cli) REFERENCES CLIENTES(id_cli)
);

-- Tabla 6: Detalles
CREATE TABLE DETALLES (
    id_ped VARCHAR(10),
    id_prod VARCHAR(10),
    cantidad INT,
    precio_unitario DECIMAL(10,2),
    descuento DECIMAL(10,2) DEFAULT 0,
    PRIMARY KEY (id_ped, id_prod),
    FOREIGN KEY (id_ped) REFERENCES PEDIDOS(id_ped),
    FOREIGN KEY (id_prod) REFERENCES PRODUCTOS(id_prod)
);

-- Tabla 7: Envíos (NUEVA - Logística)
CREATE TABLE ENVIOS (
    id_envio SERIAL PRIMARY KEY,
    id_ped VARCHAR(10),
    paqueteria VARCHAR(50), -- DHL, FedEx, etc.
    codigo_rastreo VARCHAR(50),
    fecha_salida DATE,
    FOREIGN KEY (id_ped) REFERENCES PEDIDOS(id_ped)
);

-- Tabla 8: Reseñas (NUEVA - Feedback)
CREATE TABLE RESENAS (
    id_resena SERIAL PRIMARY KEY,
    id_prod VARCHAR(10),
    id_cli VARCHAR(10),
    calificacion INT CHECK (calificacion BETWEEN 1 AND 5),
    comentario TEXT,
    fecha DATE,
    FOREIGN KEY (id_prod) REFERENCES PRODUCTOS(id_prod),
    FOREIGN KEY (id_cli) REFERENCES CLIENTES(id_cli)
);

-- ==========================================
-- 3. POBLADO DE DATOS ESTRATÉGICOS (Manuales)
-- ==========================================

-- Categorías
INSERT INTO CATEGORIAS VALUES 
('C1', 'Laptops', 'Portátiles', 16),
('C2', 'Smartphones', 'Teléfonos', 16),
('C3', 'Tablets', 'Dispositivos táctiles', 16),
('C4', 'Accesorios', 'Periféricos', 16),
('C5', 'Audio', 'Sonido', 16);

-- Proveedores (Nuevos datos)
INSERT INTO PROVEEDORES VALUES
('PR01', 'TechData', 'Carlos Slim', 'Mexico'),
('PR02', 'Ingram', 'John Doe', 'USA'),
('PR03', 'Compumundo', 'Ana Banana', 'España');

-- Clientes Clave (Para que funcionen tus consultas específicas)
INSERT INTO CLIENTES VALUES
('CLI01', 'Juan', 'Pérez', 'juan@mail.com', 'CDMX', '555-0001'),
('CLI02', 'Ana', 'Gómez', 'ana@mail.com', 'Monterrey', '811-0002'),
('CLI03', 'Luis', 'López', 'luis@mail.com', 'Guadalajara', NULL),
('CLI04', 'María', 'Díaz', 'maria@mail.com', 'CDMX', '555-0004'),
('CLI05', 'Pedro', 'Ruíz', 'pedro@mail.com', 'Puebla', NULL);

-- Productos
INSERT INTO PRODUCTOS VALUES
('P01', 'MacBook Air', 'Apple', 999.00, 50, 'C1', 'PR02'),
('P02', 'Galaxy S23', 'Samsung', 850.00, 30, 'C2', 'PR01'),
('P03', 'iPhone 15', 'Apple', 1100.00, 100, 'C2', 'PR02'),
('P04', 'iPad Air', 'Apple', 600.00, 25, 'C3', 'PR02'),
('P05', 'Galaxy Tab', 'Samsung', 500.00, 40, 'C3', 'PR01'),
('P06', 'Mouse MX', 'Logitech', 80.00, 200, 'C4', 'PR03'),
('P07', 'AirPods Pro', 'Apple', 250.00, 150, 'C5', 'PR02');

-- Pedidos y Detalles (Casos Borde para División)
INSERT INTO PEDIDOS VALUES
('PED01', '2024-01-15', 'Entregado', 'Tarjeta', 1100.00, 'CLI01'),
('PED02', '2024-02-10', 'Entregado', 'PayPal', 850.00, 'CLI02'),
('PED03', '2024-03-05', 'Procesando', 'Tarjeta', 3000.00, 'CLI01');

INSERT INTO DETALLES VALUES
('PED01', 'P04', 1, 600.00, 0), -- Juan compró iPad
('PED01', 'P05', 1, 500.00, 0), -- Juan compró Galaxy Tab (TIENE TODAS LAS TABLETS)
('PED02', 'P02', 1, 850.00, 0),
('PED03', 'P01', 3, 999.00, 50);

-- Envíos de prueba
INSERT INTO ENVIOS (id_ped, paqueteria, codigo_rastreo, fecha_salida) VALUES
('PED01', 'DHL', 'MX123456', '2024-01-16'),
('PED02', 'FedEx', 'FE987654', '2024-02-11');

-- Reseñas de prueba
INSERT INTO RESENAS (id_prod, id_cli, calificacion, comentario, fecha) VALUES
('P01', 'CLI01', 5, 'Excelente laptop', '2024-03-10'),
('P02', 'CLI02', 4, 'Buena cámara', '2024-02-15');


-- ==========================================
-- 4. GENERACIÓN MASIVA AUTOMÁTICA (+100 Tuplas)
-- ==========================================

-- Generar 50 Clientes "Relleno"
INSERT INTO CLIENTES (id_cli, nombre, apellido, email, ciudad, telefono)
SELECT 
    'C'||x, 
    'Cliente'||x, 
    'Apellido'||x, 
    'user'||x||'@test.com', 
    (ARRAY['CDMX','Monterrey','Guadalajara','Cancun'])[floor(random()*4)+1],
    '555-'||(1000+x)
FROM generate_series(10, 60) AS x;

-- Generar 50 Pedidos "Relleno" vinculados a esos clientes
INSERT INTO PEDIDOS (id_ped, fecha, estado, metodo_pago, total, id_cli)
SELECT 
    'P'||x, 
    CURRENT_DATE - (x || ' days')::interval, -- Fechas aleatorias atrás
    (ARRAY['Entregado','Enviado','Procesando','Cancelado'])[floor(random()*4)+1],
    (ARRAY['Tarjeta','PayPal','Efectivo'])[floor(random()*3)+1],
    (random()*1000)::decimal(10,2),
    'C'||(floor(random()*50)+10) -- Vincula a cliente C10...C60
FROM generate_series(100, 150) AS x;

-- Generar 100 Detalles aleatorios
INSERT INTO DETALLES (id_ped, id_prod, cantidad, precio_unitario)
SELECT 
    'P'||(floor(random()*50)+100), -- Pedido P100...P150
    'P0'||(floor(random()*7)+1),   -- Producto P01...P07
    floor(random()*5)+1,
    floor(random()*1000)+100
FROM generate_series(1, 100) AS x
ON CONFLICT DO NOTHING; -- Ignora si sale un duplicado (PK compuesta)
