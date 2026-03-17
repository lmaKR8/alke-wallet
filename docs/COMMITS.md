# Estructura de Commits — Alke Wallet Etapa 3

> Convenciones semánticas basadas en `fuente-verdad/convenciones-git.md`  
> Formato: `tipo(alcance): descripción`

---

## Formato

```
tipo(alcance): descripción breve en español (máx. 72 caracteres)

[Cuerpo opcional: qué y por qué, no el cómo]

[Footer opcional: referencias a issues, breaking changes]
```

---

## Tipos de Commit

| Tipo       | Uso                                          |
| ---------- | -------------------------------------------- |
| `feat`     | Nueva funcionalidad                          |
| `fix`      | Corrección de bug                            |
| `chore`    | Tareas de configuración / mantenimiento      |
| `style`    | Cambios de formato/estilo sin afectar lógica |
| `docs`     | Documentación                                |
| `test`     | Tests                                        |
| `refactor` | Refactorización sin cambio funcional         |
| `build`    | Cambios en dependencias o sistema de build   |
| `perf`     | Mejoras de rendimiento                       |
| `hotfix`   | Corrección urgente en producción             |
| `revert`   | Revertir commit anterior                     |

---

## Alcances (Scopes)

| Scope          | Área afectada                                        |
| -------------- | ---------------------------------------------------- |
| `config`       | `settings.py`, `urls.py`, `middleware.py`, `apps.py` |
| `accounts`     | App `apps/accounts/`                                 |
| `wallet`       | App `apps/wallet/`                                   |
| `transactions` | App `apps/transactions/`                             |
| `contacts`     | App `apps/contacts/`                                 |
| `templates`    | Carpeta `templates/` y herencia                      |
| `static`       | Carpeta `static/` (CSS, JS, imágenes)                |
| `fixtures`     | Carpeta `fixtures/` (seed data)                      |
| `migrations`   | Archivos de migración                                |
| `admin`        | Registros en panel de administración                 |
| `tests`        | Archivos de tests por app                            |
| `docs`         | Documentación (`docs/`, `README.md`)                 |

---

## Historial de Commits — Etapa 3

### Fase 1 — Configuración del Proyecto

```bash
chore(config): configurar settings.py con PostgreSQL y apps registradas
chore(config): crear AppConfig y __init__.py para las 4 apps
```

### Fase 2 — Modelos ORM

```bash
feat(wallet): crear mixin SoftDeleteModel con manager personalizado
feat(accounts): crear modelo User extendiendo AbstractUser con soft delete
feat(wallet): crear modelos Currency y Account con soft delete
feat(transactions): crear modelo Transaction con FKs a Account
```

### Fase 3 — Migraciones y Fixtures

```bash
chore(migrations): generar y aplicar migraciones iniciales
feat(fixtures): crear fixtures JSON para currencies, users, accounts y transactions
```

### Fase 4 — Autenticación y Middleware

```bash
feat(accounts): crear formularios RegisterForm y LoginForm
feat(accounts): implementar vistas login, register y logout
chore(config): crear middleware LoginRequiredMiddleware global
```

### Fase 5 — Vistas y Templates (MVT)

```bash
feat(templates): crear base.html con herencia y componentes includes
feat(wallet): implementar landing page y vista index
feat(accounts): crear templates de login y register
feat(wallet): implementar dashboard con resumen de saldo
feat(wallet): implementar deposito con creacion de transaccion
feat(transactions): implementar historial con filtros Q y paginacion
feat(contacts): implementar busqueda de contactos con Model Q
feat(contacts): implementar envio de dinero atomico con transaction.atomic
```

### Fase 6 — Estilos

```bash
style(static): migrar CSS personalizado desde Etapa 1
style(static): agregar JavaScript minimo para interacciones Bootstrap
```

### Fase 7 — Admin + URLs

```bash
feat(admin): registrar modelos en panel de administracion
chore(config): configurar URLs raiz del proyecto con includes de 4 apps
```

### Fase 8 — Testing

```bash
test(accounts): tests de modelo User, login y registro
test(wallet): tests de deposito, soft delete y dashboard
test(transactions): tests de historial con filtros y paginacion
test(contacts): tests de busqueda y transferencia atomica
```

### Fase 9 — Documentación

```bash
docs(readme): actualizar README.md con instrucciones de Etapa 3
docs(diagrama): crear diagrama de clases UML del proyecto
```

---

## Ejemplos Completos

```bash
# Commit simple
feat(wallet): implementar deposito con creacion de transaccion

# Commit con cuerpo
feat(contacts): implementar envio de dinero atomico con transaction.atomic

Usa django.db.transaction.atomic() para garantizar consistencia de saldos.
Si falla cualquier operacion (save sender, save receiver, create Transaction)
se hace rollback completo. Evita inconsistencias en caso de error parcial.

# Commit de fix
fix(transactions): corregir filtro Q para transacciones de deposito

Los depositos tienen sender_account=None. El filtro anterior excluia
los depositos del historial del usuario receptor.

# Commit de refactor
refactor(wallet): extraer calculo de saldo total a metodo del modelo Account
```

---

## Convención de Ramas

```
main                    ← Código estable / producción
develop                 ← Integración continua
feature/etapa3-config   ← Fase 1: Configuración
feature/etapa3-models   ← Fase 2: Modelos ORM
feature/etapa3-auth     ← Fase 4: Autenticación
feature/etapa3-mvt      ← Fase 5: Vistas y Templates
feature/etapa3-tests    ← Fase 8: Testing
```
