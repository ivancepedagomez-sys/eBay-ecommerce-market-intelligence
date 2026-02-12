--Esquema de Base de Datos para el Monitor de Precios
--Autor: Iván Cepeda
--Fecha: Febrero 2026

--1. Tabla principal: Precios de Competencia
--Almacena los datos crudos extraídos de la API/Scraping

CREATE TABLE IF NOT EXISTS precios_competencia (
    id SERIAL PRIMARY KEY,                                  --Identificador único autoincremental
    item_id VARCHAR(50) NOT NULL,                           --ID único del producto en la plataforma
    titulo TEXT,                                            --Título en la publicación
    precio DECIMAL(10,2),                                   --Precio con dos decimales
    moneda VARCHAR(5) DEFAULT 'EUR',                        --Divisa (EUR, USD)
    vendedor VARCHAR(100),                                  --Nombre de la tienda o vendedor
    fecha_extraccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP    --Cuándo se obtuvo el dato

);

--2. Índice para mejorar la velocidad de las consultas por fecha
CREATE INDEX idx_fecha ON precios_competencia(fecha_extraccion);