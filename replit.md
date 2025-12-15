# Pet Shop Amigo - Site Institucional

## Visão Geral
Site institucional moderno para pet shop desenvolvido em Django FullStack, com design responsivo mobile-first e painel administrativo customizado (sem Django Admin nativo).

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
├── INSTRUCOES_WHATSAPP.txt
├── core/                    # Configurações Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── pages/              # Páginas institucionais
│   ├── services/           # Serviços do pet shop
│   └── admin_panel/        # Painel administrativo customizado
├── templates/
│   ├── base.html
│   ├── pages/
│   ├── services/
│   └── admin_panel/        # Templates do painel admin
└── static/
    └── css/
        ├── style.css       # Estilos do site público
        └── admin.css       # Estilos do painel admin
```

## Apps
1. **pages**: Páginas institucionais (Home, Sobre, Contato)
2. **services**: Gerenciamento de serviços
3. **admin_panel**: Painel administrativo customizado

## Models
### Service (apps.services)
- `name`: Nome do serviço
- `description`: Descrição
- `price`: Preço (DecimalField)
- `is_active`: Status ativo/inativo
- `created_at`: Data de criação

### Testimonial (apps.admin_panel)
- `author_name`: Nome do autor
- `service`: Serviço avaliado (FK)
- `rating`: Nota (1-5)
- `comment`: Comentário
- `status`: pending/approved/rejected
- `created_at`: Data de criação

## Painel Administrativo Customizado
- URL: `/admin-panel/`
- Usuário: `admin`
- Senha: `admin123`

### Funcionalidades:
- Dashboard com estatísticas
- CRUD completo de serviços
- Gestão de depoimentos (aprovar/reprovar)
- Controle de permissões (is_staff ou is_superuser)

### Rotas do Painel:
- `/admin-panel/` - Dashboard
- `/admin-panel/services/` - Gerenciar serviços
- `/admin-panel/testimonials/` - Gerenciar depoimentos

## URLs Públicas
- `/` - Página inicial
- `/sobre/` - Sobre nós
- `/servicos/` - Lista de serviços
- `/contato/` - Contato

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
- Admin: Painel customizado (sem Django Admin nativo)
