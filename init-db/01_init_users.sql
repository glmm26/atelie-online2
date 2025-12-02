--
-- PostgreSQL database dump
--

-- Dumped from database version 15.14 (Debian 15.14-1.pgdg13+1)
-- Dumped by pg_dump version 15.14 (Debian 15.14-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', 'public', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Create usuarios table if it doesn't exist
--
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT false,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    foto VARCHAR(255)
);

--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

-- Garante que a sequência está no valor correto
-- Ensure the sequence has a valid value. If the table is empty, initialize
-- the sequence so the next nextval will return 1. If the table has rows,
-- set the sequence to the current max(id) so the next value will be max+1.
DO $$
BEGIN
    IF (SELECT COUNT(*) FROM usuarios) = 0 THEN
        PERFORM setval('usuarios_id_seq', 1, false);
    ELSE
        PERFORM setval('usuarios_id_seq', (SELECT MAX(id) FROM usuarios), true);
    END IF;
END
$$;

-- Insere o usuário apenas se ele não existir
INSERT INTO usuarios (id, nome, email, senha_hash, is_admin, data_criacao, foto)
VALUES (1, 'gui', 'guilhermef512435@gmail.com', 
        'pbkdf2:sha256:600000$4ugh0Diku0lguKnz$e497d896611ac2aa43761265f8b6251b8ae6828462e71269a644279a0fa91368',
        true, '2025-10-28 04:25:08.887097', 'user_1.jpg')
ON CONFLICT (id) DO NOTHING;