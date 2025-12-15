# Pet Shop Amigo - Site Institucional

## Visão Geral
Site institucional moderno para pet shop desenvolvido em Django FullStack, com design responsivo mobile-first e painel administrativo completo.

## Tecnologias
- **Backend**: Python 3.11, Django 5.x
- **Banco de dados**: SQLite
- **Frontend**: Django Templates, HTML5, CSS3
- **Servidor**: Django Development Server

## Estrutura do Projeto
```
petshop/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── core/                 # Configurações Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── pages/           # Páginas institucionais (Home, Sobre, Contato)
│   └── services/        # Serviços do pet shop
├── templates/           # Templates globais
│   ├── base.html
│   ├── pages/
│   └── services/
└── static/
    └── css/style.css
```

## Apps
1. **pages**: Páginas institucionais (Home, Sobre, Contato) - sem models
2. **services**: Gerenciamento de serviços com modelo Service

## Modelo Service
- `name`: Nome do serviço
- `description`: Descrição
- `price`: Preço (DecimalField)
- `is_active`: Status ativo/inativo
- `created_at`: Data de criação

## Painel Administrativo
- URL: `/admin/`
- Usuário: `admin`
- Senha: `admin123`

Funcionalidades:
- CRUD completo de serviços
- Filtros por status e data
- Busca por nome
- Edição inline de status

## URLs
- `/` - Página inicial
- `/sobre/` - Sobre nós
- `/servicos/` - Lista de serviços
- `/contato/` - Contato
- `/admin/` - Painel administrativo

## Executar o Projeto
```bash
python manage.py runserver 0.0.0.0:5000
```

## Design
- Mobile-first responsivo
- Paleta: Roxo (#7C3AED) e Verde (#10B981)
- Integração WhatsApp
- Cards de serviços dinâmicos

## Preferências do Usuário
- Idioma: Português (Brasil)
- Framework: Django (sem frameworks JS adicionais)
- Banco: SQLite (simplicidade)
