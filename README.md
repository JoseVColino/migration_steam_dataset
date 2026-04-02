# 🎮 Steam Games — Banco de Dados PostgreSQL

Projeto acadêmico de modelagem e implementação de um banco de dados relacional a partir do dataset público da Steam, desenvolvido para a disciplina de Banco de Dados do curso de Engenharia de Computação.

---

## 📋 Sobre o Projeto

O dataset contém informações de mais de 18.000 jogos da plataforma Steam, com 39 colunas cobrindo dados como avaliações, tempo de jogo, desenvolvedores, publishers, gêneros, tags, categorias, idiomas, plataformas e muito mais.

O objetivo foi projetar um banco de dados normalizado em PostgreSQL, popular as tabelas a partir do CSV original usando Python, e responder consultas analíticas com SQL.

---

## 🗂️ Estrutura do Repositório

```
📦 steam-database
 ┣ 📁 python_scripts        # Scripts Python para popular o banco
 ┣ 📄 ddl.sql               # Script de criação das tabelas (DDL)
 ┗ 📄 README.md
```

---
 
## 🏗️ Modelagem
 
O banco foi normalizado seguindo as boas práticas de modelagem relacional. Colunas com múltiplos valores (como gêneros, tags, categorias e idiomas) foram extraídas para tabelas próprias com relacionamentos N:N.
 
### Tabelas principais
 
| Tabela | Descrição |
|---|---|
| `game` | Dados centrais de cada jogo |
| `reviews` | Avaliações positivas, negativas e texto |
| `metacritic` | Nota e URL do Metacritic |
 
### Tabelas de entidade (lookup)
 
| Tabela | Descrição |
|---|---|
| `company` | Desenvolvedoras e publishers |
| `categoria` | Categorias Steam (ex: Single-player, Co-op) |
| `generos` | Gêneros (ex: Action, RPG, Indie) |
| `tags` | Tags da comunidade |
| `language` | Idiomas suportados |
| `operating_system` | Sistemas operacionais (Windows, Mac, Linux) |
 
### Tabelas de relacionamento N:N
 
| Tabela | Relacionamento |
|---|---|
| `game_company` | Jogo ↔ Empresa (com campo `tipo`: developer ou publisher) |
| `game_categoria` | Jogo ↔ Categoria |
| `game_genero` | Jogo ↔ Gênero |
| `game_tag` | Jogo ↔ Tag |
| `game_languages` | Jogo ↔ Idioma |
| `game_operating_system` | Jogo ↔ Sistema operacional |
 
### Tabelas de mídia
 
| Tabela | Descrição |
|---|---|
| `screenshots` | URLs de screenshots de cada jogo |
| `movies` | URLs de trailers/vídeos de cada jogo |
 
---

## 👥 Equipe

| Nome | GitHub |
|---|---|
| Ana Alice Dias Conde | |
| Caio Vasconcelos Braga | |
| José Victor Colino Gonçalves | |
| Yasmin dos Santos Barata | [@YasminSBarata](https://github.com/YasminSBarata) |

---

## 📚 Dataset

Dataset público da Steam disponível no Kaggle:  
[Steam Games Dataset](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset)
