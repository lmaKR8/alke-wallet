# Alke Wallet — Billetera Digital con Django

## Índice

- [Autor](#autor)
- [Documentación Adicional](#documentación-adicional)
- [Descripción del Proyecto](#descripción-del-proyecto)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Conceptos de Django Aplicados](#conceptos-de-django-aplicados)
- [Funcionalidades Implementadas](#funcionalidades-implementadas)
- [Modelos de Datos (ORM)](#modelos-de-datos-orm)
- [Base de Datos PostgreSQL (Etapa 2)](#base-de-datos-postgresql-etapa-2)
- [Uso del Sistema](#uso-del-sistema)
- [Testing](#testing)
- [Convenciones de Código](#convenciones-de-código)
- [Ramas del Proyecto](#ramas-del-proyecto)

---

## Autor

**Desarrollado por**: Leandro Marchant A.
**Tipo**: Proyecto Educativo
**Módulo**: Desarrollo Web con Django — Fundamentos y Modelos
**Programa**: Fullstack Python — Talento Digital
**Año**: 2026

---

## Documentación Adicional

| Documento | Descripción |
| --------- | ----------- |
| `docs/diagrama_clases_alke-wallet.md` | Documentación detallada del diagrama de clases |
| `docs/diagrama_clases_alke-wallet.puml` | Diagrama de clases UML (PlantUML) |
| `docs/COMMITS.md` | Convenciones de commits semánticos e historial de fases |

## Descripción del Proyecto

**Alke Wallet** es una aplicación web de billetera digital desarrollada con el framework Django como proyecto final del módulo de Desarrollo Web con Django del programa **Fullstack Python — Talento Digital 2026**.

Es la tercera etapa de evolución del proyecto:

| Etapa | Entregable | Stack | Repositorio |
| ----- | ---------- | ----- | ----------- |
| **Etapa 1** | Frontend estático (Landing, Login, Dashboard, Depósito, Enviar dinero, Historial) | HTML5, CSS3, Bootstrap 5, jQuery, LocalStorage | [alke-wallet-mvp](https://github.com/lmaKR8/alke-wallet-mvp) |
| **Etapa 2** | Base de datos relacional con PostgreSQL, Soft Delete y vistas analíticas | PostgreSQL, SQL puro | [alke-wallet-bd](https://github.com/lmaKR8/alke-wallet-bd) |
| **Etapa 3** | Aplicación Django completa unificando Etapa 1 y Etapa 2 | Django 6.0.3, Python 3.14, SQLite/PostgreSQL | [alke-wallet](https://github.com/lmaKR8/alke-wallet) |

### El Desafío

**Alke Solutions**, una empresa de desarrollo de software, necesita construir una aplicación web completa con Django. El objetivo es demostrar el dominio del framework en sus capas fundamentales:

- Modelar la base de datos con el ORM de Django, replicando el esquema físico de la Etapa 2
- Implementar autenticación real con modelo `User` personalizado (email en lugar de username)
- Aplicar el patrón **Soft Delete** en todos los modelos de negocio
- Usar **Model Q** para filtros dinámicos con condiciones OR/AND compuestas
- Implementar **transferencias atómicas** con `transaction.atomic()`
- Proteger rutas con middleware global de autenticación
- Estructurar el proyecto con 4 apps modulares bajo el patrón **MVT**
- Cubrir funcionalidades clave con **tests de integración**

### Solución Implementada

Aplicación web modular con Django que integra:

- **4 apps Django** bajo `apps/` (`accounts`, `wallet`, `transactions`, `contacts`)
- **Modelo User personalizado** con email como campo de autenticación, extendiendo `AbstractUser`
- **Mixin `SoftDeleteModel`** compartido por todos los modelos de negocio (eliminación lógica)
- **4 modelos ORM** que mapean exactamente el esquema de Etapa 2: `User`, `Currency`, `Account`, `Transaction`
- **Sistema de autenticación** completo: registro, login y logout
- **Middleware global** `LoginRequiredMiddleware` que protege todas las rutas privadas
- **11 templates HTML** con herencia desde `base.html` y componentes reutilizables (`_navbar`, `_alerts`, `_footer`)
- **Historial de transacciones** con filtros dinámicos (Model Q) y paginación
- **Transferencias atómicas** con `transaction.atomic()` para garantizar consistencia de saldos
- **Búsqueda de usuarios** por nombre o email con Model Q (OR compuesto)
- **18 tests de integración** distribuidos en 3 apps (accounts, wallet, transactions)
- **Fixtures de datos demo**: 5 monedas, 15 usuarios temáticos (LOTR), 22 cuentas, 60 transacciones

---

## Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
| ---------- | ------- | --------- |
| **Python** | 3.14 | Lenguaje principal |
| **Django** | 6.0.3 | Framework web (MVT) |
| **SQLite** | Built-in | Base de datos de desarrollo |
| **PostgreSQL** | 12+ | Base de datos de producción |
| **psycopg2-binary** | 2.9.11 | Adaptador PostgreSQL para Django |
| **Bootstrap** | 5.3.2 CDN | Framework CSS responsive |
| **Bootstrap Icons** | 1.11.1 CDN | Iconografía vectorial |
| **JavaScript** | ES6 | Interacciones mínimas del lado del cliente |
| **asgiref** | 3.11.1 | Soporte ASGI de Django |
| **sqlparse** | 0.5.5 | Formateador SQL (dependencia de Django) |

---

## Estructura del Proyecto

El proyecto sigue la arquitectura MVT de Django con separación por apps:

```
alke-wallet/
│
├── manage.py                              # Script de gestión de Django
├── requirements.txt                       # Dependencias del proyecto
├── db.sqlite3                             # Base de datos SQLite (desarrollo)
├── README.md                              # Este archivo
│
├── alke_wallet/                           # Configuración del proyecto Django
│   ├── __init__.py
│   ├── settings.py                            # PostgreSQL, apps, auth, i18n, mensajes
│   ├── urls.py                                # URLs raíz con includes de 4 apps
│   ├── middleware.py                          # LoginRequiredMiddleware (protección global)
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/                                  # Aplicaciones Django (patrón modular)
│   ├── __init__.py
│   │
│   ├── accounts/                              # Autenticación y modelo User
│   │   ├── models.py                              # User (AbstractUser + SoftDeleteModel)
│   │   ├── forms.py                               # RegisterForm, LoginForm
│   │   ├── views.py                               # CustomLoginView, register_view, CustomLogoutView
│   │   ├── urls.py                                # /accounts/login|register|logout
│   │   ├── admin.py
│   │   └── tests.py                               # 4 tests: modelo, login, registro
│   │
│   ├── wallet/                                # Billetera, monedas y cuentas
│   │   ├── mixins.py                              # SoftDeleteModel + SoftDeleteManager
│   │   ├── models.py                              # Currency, Account
│   │   ├── forms.py                               # DepositForm
│   │   ├── views.py                               # index_view, dashboard_view, deposit_view
│   │   ├── urls.py                                # / | /dashboard/ | /deposit/
│   │   ├── admin.py
│   │   └── tests.py                               # 6 tests: depósito, soft delete, dashboard
│   │
│   ├── transactions/                          # Historial de transacciones
│   │   ├── models.py                              # Transaction (con FK nullable para depósitos)
│   │   ├── views.py                               # transaction_list_view (Q + Paginator)
│   │   ├── urls.py                                # /transactions/
│   │   ├── admin.py
│   │   └── tests.py                               # 4 tests: filtros, período, autenticación
│   │
│   └── contacts/                              # Búsqueda de usuarios y transferencias
│       ├── forms.py                               # SendMoneyForm
│       ├── views.py                               # contacts_view, send_money_view
│       ├── urls.py                                # /contacts/ | /contacts/send/<id>/
│       └── tests.py
│
├── templates/                             # Templates globales
│   ├── base.html                              # Template raíz (Bootstrap 5.3.2 CDN)
│   ├── includes/                              # Fragmentos reutilizables
│   │   ├── _navbar.html                           # Navegación condicional (auth/anon)
│   │   ├── _alerts.html                           # Mensajes Django → Bootstrap alerts
│   │   └── _footer.html                           # Footer común
│   ├── landing/
│   │   └── index.html                             # Landing page pública
│   ├── accounts/
│   │   ├── login.html                             # Formulario de inicio de sesión
│   │   └── register.html                          # Formulario de registro
│   ├── wallet/
│   │   ├── dashboard.html                         # Dashboard con saldo por cuenta
│   │   └── deposit.html                           # Formulario de depósito
│   ├── transactions/
│   │   └── list.html                              # Historial con filtros y paginación
│   └── contacts/
│       ├── list.html                              # Búsqueda de usuarios
│       └── send_money.html                        # Formulario de transferencia
│
├── static/                                # Archivos estáticos
│   ├── css/
│   │   └── style.css                          # Estilos personalizados (heredados de Etapa 1)
│   ├── js/
│   │   └── main.js                            # JavaScript mínimo para Bootstrap
│   └── img/                                   # Imágenes del proyecto
│
├── fixtures/                              # Datos de demostración (seed data)
│   ├── currencies.json                        # 5 monedas: CLP, USD, EUR, CNY, CAD
│   ├── users.json                             # 15 usuarios (temática El Señor de los Anillos)
│   ├── accounts.json                          # 22 cuentas en distintas monedas
│   └── transactions.json                      # 60 transacciones (depósitos y transferencias)
│
├── data/                                  # Credenciales de la base de datos (ignorado por Git)
│   └── .env.db                                # Variables de entorno para la conexión a PostgreSQL
│
└── docs/                                  # Documentación técnica del proyecto
    ├── COMMITS.md                             # Convenciones de commits semánticos
    ├── diagrama_clases_alke-wallet.puml       # Diagrama de clases PlantUML
    └── diagrama_clases_alke-wallet.md         # Documentación del diagrama de clases
```

---

## Conceptos de Django Aplicados

### Modelo User Personalizado
Extensión de `AbstractUser` con `email` como campo de autenticación (`USERNAME_FIELD = 'email'`).
El campo `username` de Django es reemplazado por `user_name`. El manager personalizado
`UserManager` filtra usuarios activos mediante soft delete.

### Soft Delete (Eliminación Lógica)
`SoftDeleteModel` es un modelo abstracto en `apps/wallet/mixins.py` heredado por todos
los modelos de negocio. En lugar de eliminar registros con `DELETE`, se registra la fecha
de eliminación en `deleted_at`. El manager por defecto (`objects`) filtra automáticamente
`deleted_at IS NULL`; el manager `all_objects` permite acceder al historial completo.

```python
instancia.soft_delete()  # deleted_at = timezone.now()
instancia.restore()      # deleted_at = None
instancia.is_deleted     # True si deleted_at no es None
```

### Model Q — Filtros Dinámicos
Usado en `transaction_list_view` y `contacts_view` para construir consultas con condiciones
OR/AND compuestas en tiempo de ejecución, sin concatenar cadenas SQL.

```python
# Historial: transacciones donde el usuario es remitente O receptor
base_query = Q(sender_account_id__in=ids) | Q(receiver_account_id__in=ids)

# Búsqueda de contactos por nombre O email
search_query = Q(user_name__icontains=term) | Q(email__icontains=term)
```

### Transferencias Atómicas
`send_money_view` usa `transaction.atomic()` para garantizar que si cualquier paso
de la transferencia falla (descuento del sender, acreditación del receiver o creación
del registro `Transaction`), se hace rollback completo y el saldo queda sin modificar.

```python
with transaction.atomic():
    sender_account.withdraw(amount)
    receiver_account.deposit(amount)
    Transaction.objects.create(...)
```

### Middleware Global de Autenticación
`LoginRequiredMiddleware` en `alke_wallet/middleware.py` intercepta cada request y
redirige a `/accounts/login/?next=<ruta>` si el usuario no está autenticado, sin
necesidad de aplicar `@login_required` en cada vista individualmente. Las rutas
públicas (landing, login, registro, admin, static) están explícitamente excluidas.

### Paginación Django
`transaction_list_view` usa `Paginator` de Django para paginar el historial de
transacciones a 5 registros por página, manteniendo el estado de los filtros
de tipo y período entre páginas.

### Sistema de Mensajes → Bootstrap
`MESSAGE_TAGS` en `settings.py` mapea los niveles de mensajes de Django a clases
Bootstrap (`error` → `danger`, `debug` → `secondary`, etc.), integrados en el
componente `_alerts.html`.

### Herencia de Templates
Todos los templates extienden `base.html` con bloques `{% block title %}`,
`{% block content %}` y `{% block extra_css/js %}`. Los componentes
`_navbar.html`, `_footer.html` y `_alerts.html` se incluyen con `{% include %}`.

---

## Funcionalidades Implementadas

### Autenticación
- Registro de usuarios con validación de contraseña y email único
- Inicio de sesión con email como identificador (no username)
- Cierre de sesión con mensaje de confirmación
- Protección global de rutas privadas vía middleware

### Dashboard
- Visualización de todas las cuentas activas del usuario por moneda
- Cuenta principal CLP destacada con saldo actual
- Accesos rápidos a Depositar, Enviar y Transacciones
- Listado de las últimas transacciones recientes

### Depósitos
- Formulario con validación de monto positivo (`DecimalField`)
- Creación de `Transaction` con `sender_account=None` (depósito externo)
- Actualización atómica del saldo de la cuenta receptora
- Redirección al dashboard con mensaje de confirmación

### Historial de Transacciones
- Vista completa de movimientos del usuario (depósitos, envíos y recibidos)
- Filtro por tipo: Todos / Depósito / Envío / Recibido
- Filtro por período: 7 / 30 / 90 / 365 días
- Resumen de totales: total ingresado y total enviado
- Paginación de 5 resultados por página con navegación

### Contactos y Envío de Dinero
- Búsqueda de usuarios por nombre o email (Model Q con OR)
- Transferencia de dinero con validación de saldo suficiente
- Operación atómica: si falla un paso, no se modifica ningún saldo
- Verificación de que el receptor tenga cuenta en la misma moneda

---

## Modelos de Datos (ORM)

El ORM replica exactamente el esquema físico de la Etapa 2 (PostgreSQL):

### SoftDeleteModel (Mixin abstracto — `apps/wallet/mixins.py`)

| Campo | Tipo | Descripción |
| ----- | ---- | ----------- |
| `created_at` | DateTimeField | Timestamp de creación (auto) |
| `updated_at` | DateTimeField | Timestamp de modificación (auto) |
| `deleted_at` | DateTimeField | NULL = activo / fecha = eliminado lógicamente |

### User (`apps/accounts/models.py`)

| Campo E2 | Campo Django | Tipo |
| -------- | ------------ | ---- |
| `id_user` | `id` (PK auto) | AutoField |
| `user_name` | `user_name` | CharField(60) |
| `email` | `email` | EmailField(100, UNIQUE) |
| `password` | `password` | Heredado de AbstractUser (con hash) |
| `created_at` | Mixin | DateTimeField |
| `updated_at` | Mixin | DateTimeField |
| `deleted_at` | Mixin | DateTimeField(null) |

### Currency (`apps/wallet/models.py`)

| Campo E2 | Campo Django | Tipo |
| -------- | ------------ | ---- |
| `id_currency` | `id` (PK auto) | AutoField |
| `currency_name` | `currency_name` | CharField(50, UNIQUE) |
| `currency_symbol` | `currency_symbol` | CharField(3, UNIQUE) |

### Account (`apps/wallet/models.py`)

| Campo E2 | Campo Django | Tipo |
| -------- | ------------ | ---- |
| `id_account` | `id` (PK auto) | AutoField |
| `user_id` | `user` | FK → User (CASCADE) |
| `currency_id` | `currency` | FK → Currency (PROTECT) |
| `balance` | `balance` | DecimalField(12, 2, default=0) |

### Transaction (`apps/transactions/models.py`)

| Campo E2 | Campo Django | Tipo |
| -------- | ------------ | ---- |
| `id_transaction` | `id` (PK auto) | AutoField |
| `sender_account_id` | `sender_account` | FK → Account (null=True) |
| `receiver_account_id` | `receiver_account` | FK → Account (CASCADE) |
| `amount` | `amount` | DecimalField(12, 2) |
| `transaction_date` | `transaction_date` | DateTimeField(auto_now_add) |

> `sender_account = NULL` indica un depósito externo (sin cuenta de origen).
> `sender_account != NULL` indica una transferencia entre usuarios.

---

## Base de Datos PostgreSQL (Etapa 2)

La Etapa 2 implementó este mismo esquema de datos directamente en PostgreSQL usando SQL puro,
sin ORM. Los cuatro modelos anteriores replican fielmente ese esquema físico.
Repositorio completo: [alke-wallet-bd](https://github.com/lmaKR8/alke-wallet-bd).

### Conceptos SQL Aplicados

- Creación de tablas con constraints (`PRIMARY KEY`, `UNIQUE`, `NOT NULL`)
- Claves primarias auto-incrementales (`SERIAL`) y foráneas entre tablas
- Tipos de datos: `SERIAL`, `VARCHAR`, `NUMERIC(12,2)`, `TIMESTAMP`
- Inserción masiva con `INSERT INTO` multi-fila
- Consultas con `SELECT`, `WHERE`, `ORDER BY`
- `INNER JOIN` y `LEFT JOIN` para relacionar las 4 tablas
- Funciones de agregación: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`
- `GROUP BY` y `HAVING` para agrupaciones con filtro
- Operadores lógicos: `AND`, `OR`, `NOT`
- Filtros condicionales con `CASE WHEN`
- Funciones de ventana: `ROW_NUMBER() OVER`
- Creación de vistas optimizadas con `CREATE VIEW`
- Soft Delete mediante columna `deleted_at`

### Estructura de Tablas (PostgreSQL)

| Tabla | PK | FKs | Constraints clave |
| ----- | -- | --- | ----------------- |
| `users` | `id_user SERIAL` | — | `UNIQUE(email)` |
| `currencies` | `id_currency SERIAL` | — | `UNIQUE(currency_name)`, `UNIQUE(currency_symbol)` |
| `accounts` | `id_account SERIAL` | `user_id → users`, `currency_id → currencies` | — |
| `transactions` | `id_transaction SERIAL` | `sender_account_id → accounts` (nullable), `receiver_account_id → accounts` | — |

### Vistas Analíticas

#### Top 5 Usuarios con Mayor Saldo

```sql
CREATE OR REPLACE VIEW vw_top5_usuarios_mayor_saldo AS
SELECT
    ROW_NUMBER() OVER (ORDER BY SUM(a.balance) DESC) AS ranking,
    u.user_name,
    u.email,
    SUM(a.balance)    AS saldo_total,
    MAX(a.updated_at) AS ultima_actualizacion
FROM users u
INNER JOIN accounts a   ON u.id_user     = a.user_id
INNER JOIN currencies c ON a.currency_id = c.id_currency
WHERE u.deleted_at IS NULL
GROUP BY u.id_user, u.user_name, u.email
ORDER BY saldo_total DESC
LIMIT 5;
```

#### Top 10 Usuarios con Mayor Actividad Transaccional

```sql
CREATE OR REPLACE VIEW vw_top_usuarios_actividad AS
SELECT
    ROW_NUMBER() OVER (ORDER BY COUNT(t.id_transaction) DESC) AS ranking,
    u.user_name,
    COUNT(DISTINCT t.id_transaction) AS total_transacciones,
    ROUND(AVG(t.amount), 2)          AS monto_promedio_transacciones
FROM users u
INNER JOIN accounts a ON u.id_user        = a.user_id
LEFT JOIN  transactions t ON a.id_account = t.sender_account_id
WHERE u.deleted_at IS NULL
GROUP BY u.id_user, u.user_name
HAVING COUNT(DISTINCT t.id_transaction) > 0
ORDER BY total_transacciones DESC
LIMIT 10;
```

---

## Uso del Sistema

### Requisitos

- Python 3.11 o superior
- pip (gestor de paquetes)
- Para producción: PostgreSQL 12 o superior

### Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/lmaKR8/alke-wallet.git
cd alke-wallet

# 2. Crear y activar el entorno virtual
python -m venv env
source env/Scripts/activate       # Windows
# source env/bin/activate          # Linux/macOS

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Crear el archivo de credenciales PostgreSQL (ignorado por Git, debe crearse manualmente)
# Crear data/.env.db con el siguiente contenido:
# DB_NAME=alke_wallet
# DB_USER=postgres
# DB_PASSWORD=tu_password
# DB_HOST=localhost
# DB_PORT=5432

# 5. Aplicar migraciones
python manage.py migrate

# 6. Cargar datos de demostración
python manage.py loaddata currencies users accounts transactions

# 7. Iniciar el servidor de desarrollo
python manage.py runserver
```

Acceder a [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Credenciales de Acceso (Fixtures)

El sistema incluye 15 usuarios de demostración con temática de El Señor de los Anillos:

```
Email:    frodo.bolson@shire.me
Password: password123
```

### URLs Disponibles

| URL | Vista | Descripción |
| --- | ----- | ----------- |
| `/` | `index_view` | Landing page pública |
| `/accounts/login/` | `CustomLoginView` | Inicio de sesión |
| `/accounts/register/` | `register_view` | Registro de nuevo usuario |
| `/accounts/logout/` | `CustomLogoutView` | Cierre de sesión |
| `/dashboard/` | `dashboard_view` | Panel principal (login requerido) |
| `/deposit/` | `deposit_view` | Formulario de depósito (login requerido) |
| `/transactions/` | `transaction_list_view` | Historial con filtros (login requerido) |
| `/contacts/` | `contacts_view` | Búsqueda de usuarios (login requerido) |
| `/contacts/send/<id>/` | `send_money_view` | Transferencia a usuario (login requerido) |
| `/admin/` | Django Admin | Panel de administración |

---

## Testing

El proyecto incluye **18 tests de integración** distribuidos en 3 apps:

### Ejecutar todos los tests

```bash
python manage.py test apps
```

### Cobertura por App

| App | Tests | Qué verifica |
| --- | ----- | ------------ |
| `accounts` | 4 | Modelo User (USERNAME_FIELD), login válido/inválido, creación de usuario vía registro |
| `wallet` | 6 | Depósito crea Transaction, depósito actualiza saldo, monto inválido, soft delete, exclusión de queryset, dashboard requiere login |
| `transactions` | 4 | Vista sin filtros devuelve 200, filtro por tipo, filtro por período, protección de ruta |

### Descripción de Tests Clave

```python
# accounts — verifica autenticación con email
test_user_model_email_login        # USERNAME_FIELD == 'email'
test_login_valid_credentials       # POST /login/ → redirige al dashboard
test_login_invalid_credentials     # POST /login/ con clave incorrecta → 200
test_register_creates_user         # POST /register/ → crea usuario en BD

# wallet — verifica depósitos y soft delete
test_deposit_creates_transaction   # POST /deposit/ → Transaction con sender=None
test_deposit_updates_balance       # POST /deposit/ → balance += amount
test_deposit_invalid_amount        # POST /deposit/ monto=0 → sin cambios
test_soft_delete_account           # .soft_delete() → deleted_at != None
test_soft_delete_excludes_from_queryset  # .objects.filter() excluye eliminados
test_dashboard_requires_login      # GET /dashboard/ sin sesión → redirige

# transactions — verifica filtros y protección de ruta
test_transaction_list_no_filter    # GET /transactions/ → 200 con page_obj
test_transaction_list_filter_type  # ?tipo=envio → solo envíos del usuario
test_transaction_list_filter_period  # ?periodo=7 → solo últimos 7 días
test_transaction_list_requires_login  # sin sesión → redirige al login
```

---

## Convenciones de Código

El proyecto sigue las convenciones definidas en `docs/COMMITS.md`:

### Python
- **PEP 8** en todo el código
- **Docstrings obligatorios** en cada función, clase y método
- **snake_case** para variables y funciones; **PascalCase** para clases
- Imports ordenados: stdlib → django → apps locales, separados por línea en blanco

### Django / Templates
- Nombres de URL siempre con `name=` y en `snake_case`
- `{% url 'nombre' %}` para todas las URLs (nunca hardcodeadas)
- Sin lógica de negocio en templates — solo presentación
- Cada vista retorna `render(request, template, context)` o `redirect('nombre')`

### Commits Semánticos
Formato: `tipo(alcance): descripción breve en español (máx. 72 caracteres)`

| Tipo | Uso |
| ---- | --- |
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de bug |
| `chore` | Configuración / mantenimiento |
| `style` | Cambios de formato sin afectar lógica |
| `docs` | Documentación |
| `test` | Tests |
| `refactor` | Refactorización sin cambio funcional |

---

## Ramas del Proyecto

| Rama | Descripción | Estado |
| ---- | ----------- | ------ |
| `main` | Rama principal de producción | Activa |
| `develop` | Integración continua | Activa |
| `feature/etapa3-config` | Fase 1: Configuración del proyecto | Mergeada |
| `feature/etapa3-models` | Fase 2: Modelos ORM y migraciones | Mergeada |
| `feature/etapa3-auth` | Fase 4: Autenticación y middleware | Mergeada |
| `feature/etapa3-mvt` | Fase 5: Vistas y templates MVT | Mergeada |
| `feature/etapa3-tests` | Fase 8: Suite de tests | Mergeada |

---

*Proyecto educativo — Fullstack Python, Talento Digital 2026*
