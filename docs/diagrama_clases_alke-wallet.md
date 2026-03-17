# DIAGRAMA UML - ALKE WALLET - SISTEMA DE BILLETERA DIGITAL

---
## Índice
- [Instrucciones de Exportación](#instrucciones-de-exportación)
- [Diagrama UML - Vista General](#diagrama-uml---vista-general)
- [Leyenda de Símbolos UML](#leyenda-de-símbolos-uml)
- [SoftDeleteModel (Mixin Base)](#softdeletemodel-mixin-base)
- [SoftDeleteManager](#softdeletemanager)
- [User (Modelo de Usuario)](#user-modelo-de-usuario)
- [UserManager](#usermanager)
- [Currency (Modelo de Moneda)](#currency-modelo-de-moneda)
- [Account (Modelo de Cuenta)](#account-modelo-de-cuenta)
- [Transaction (Modelo de Transacción)](#transaction-modelo-de-transacción)
- [RegisterForm](#registerform)
- [LoginForm](#loginform)
- [DepositForm](#depositform)
- [SendMoneyForm](#sendmoneyform)

---
## Instrucciones de Exportación
### 1. Usando PlantUML Online

1. Ir a: [https://www.plantuml.com/plantuml/uml](https://www.plantuml.com/plantuml/uml)
2. Copiar el código entre `@startuml` y `@enduml` del archivo `diagrama_clases_alke-wallet.puml`
3. Descargar como PNG o SVG → guardar en `fuente-verdad/design/`

---
## Diagrama UML - Vista General

### Jerarquía de Modelos (Herencia)
```
                                ┌──────────────────────────────────┐
                                │          SoftDeleteModel         │
                                │           <<abstracto>>          │
                                ├──────────────────────────────────┤
                                │ # created_at : DateTimeField     │
                                │ # updated_at : DateTimeField     │
                                │ # deleted_at : DateTimeField     │
                                ├──────────────────────────────────┤
                                │ # objects : SoftDeleteManager    │
                                │ # all_objects : Manager          │
                                ├──────────────────────────────────┤
                                │ + soft_delete() : void           │
                                │ + restore() : void               │
                                │ + is_deleted : bool <<property>> │
                                └──────────────┬───────────────────┘
                                               │
                        ┌──────────────────────┼──────────────────────┐
                        │                      │                      │
                        ▼                      ▼                      ▼
            ┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐
            │    Currency       │  │     Account       │  │   Transaction     │
            │  (apps/wallet)    │  │  (apps/wallet)    │  │ apps/transactions │
            └───────────────────┘  └───────────────────┘  └───────────────────┘

                        También hereda (herencia múltiple):
                        AbstractUser + SoftDeleteModel
                                      │
                                      ▼
                            ┌──────────────────┐
                            │       User       │
                            │  (apps/accounts) │
                            └──────────────────┘
```

### Relaciones entre Modelos (Asociaciones FK)
```
    ┌──────────────────┐          ┌──────────────────────┐
    │       User       │ 1      * │       Account        │
    │                  │◆─────────│ user → FK → User     │
    └──────────────────┘          │ currency → FK →      │
                                  │   Currency           │
    ┌──────────────────┐          │ balance: Decimal     │
    │    Currency      │ 1      * │                      │
    │                  │◆─────────│ + deposit(amount)    │
    └──────────────────┘          │ + withdraw(amount)   │
                                  └──────────┬───────────┘
                                             │
                              ┌──────────────┴──────────────┐
                              │ 0..1 (sender, nullable)     │ 1 (receiver)
                              ▼                             ▼
                    ┌────────────────────────────────────────────────┐
                    │                 Transaction                    │
                    │  sender_account  : FK → Account (NULL=True)    │
                    │  receiver_account: FK → Account                │
                    │  amount          : DecimalField(12,2)          │
                    │  transaction_date: DateTimeField               │
                    ├────────────────────────────────────────────────┤
                    │  + transaction_type : str <<property>>         │
                    └────────────────────────────────────────────────┘
```

### Formularios (Forms — sin persistencia en BD)
```
    ┌──────────────────────┐   ┌──────────────────────┐
    │  UserCreationForm    │   │  AuthenticationForm  │
    │      <<Django>>      │   │      <<Django>>      │
    └──────────┬───────────┘   └──────────┬───────────┘
               │ hereda                   │ hereda
               ▼                          ▼
    ┌──────────────────────┐   ┌──────────────────────┐
    │    RegisterForm      │   │      LoginForm       │
    │   (apps/accounts)    │   │   (apps/accounts)    │
    └──────────────────────┘   └──────────────────────┘

    ┌──────────────────────┐   ┌──────────────────────┐
    │      forms.Form      │   │      forms.Form      │
    │      <<Django>>      │   │      <<Django>>      │
    └──────────┬───────────┘   └──────────┬───────────┘
               │ hereda                   │ hereda
               ▼                          ▼
    ┌──────────────────────┐   ┌──────────────────────┐
    │     DepositForm      │   │     SendMoneyForm    │
    │    (apps/wallet)     │   │    (apps/contacts)   │
    └──────────────────────┘   └──────────────────────┘
```

---
## Leyenda de Símbolos UML

### Visibilidad

| Símbolo | Significado |
| ------- | ----------- |
| `+`     | Público     |
| `-`     | Privado     |
| `#`     | Protegido   |

### Relaciones

| Símbolo  | Significado                                          |
| -------- | ---------------------------------------------------- |
| `──▷`    | Herencia (extends / hereda de)                       |
| `◆──`    | Composición (el contenedor es dueño del objeto)      |
| `◇──`    | Agregación / FK (referencia sin propiedad exclusiva) |
| `───`    | Asociación simple                                    |
| `- - >`  | Dependencia (usa / depende de)                       |

### Multiplicidad

| Símbolo | Significado     |
| ------- | --------------- |
| `1`     | Exactamente uno |
| `0..1`  | Cero o uno      |
| `*`     | Cero o más      |
| `0..*`  | Cero o más      |
| `1..*`  | Uno o más       |

---
## SoftDeleteModel (Mixin Base)

### Descripción
La clase abstracta `SoftDeleteModel` es el mixin base compartido por todos los modelos
de negocio de Alke Wallet. Implementa el patrón de **Soft Delete**: en lugar de eliminar
registros físicamente de la base de datos, se registra la fecha de eliminación en el campo
`deleted_at`. Si `deleted_at` es `NULL`, el registro está activo.

Se ubica en `apps/wallet/mixins.py` y todos los modelos de negocio heredan de él.

### Relación UML
```
SoftDeleteModel ──▷ Currency      (Herencia)
SoftDeleteModel ──▷ Account       (Herencia)
SoftDeleteModel ──▷ Transaction   (Herencia)
SoftDeleteModel ──▷ User          (Herencia — múltiple con AbstractUser)
SoftDeleteModel ◆── SoftDeleteManager : objects
```

### Diagrama UML
```
    ┌──────────────────────────────────────┐
    │         SoftDeleteModel              │
    │           <<abstracto>>              │
    ├──────────────────────────────────────┤
    │ # created_at : DateTimeField         │
    │ # updated_at : DateTimeField         │
    │ # deleted_at : DateTimeField         │
    ├──────────────────────────────────────┤
    │ # objects    : SoftDeleteManager     │
    │ # all_objects: Manager               │
    ├──────────────────────────────────────┤
    │ + soft_delete() : void               │
    │ + restore()    : void                │
    │ + is_deleted   : bool <<property>>   │
    └──────────────────────────────────────┘
                        ◆
                        │ composición
                        ▼
           ┌─────────────────────────┐
           │    SoftDeleteManager    │
           │  (manager por defecto)  │
           └─────────────────────────┘
```

### Campos

| Campo        | Tipo          | Opciones           | Descripción                          |
| ------------ | ------------- | ------------------ | ------------------------------------ |
| `created_at` | DateTimeField | auto_now_add=True  | Timestamp de creación (automático)   |
| `updated_at` | DateTimeField | auto_now=True      | Timestamp de modificación (auto)     |
| `deleted_at` | DateTimeField | null=True, blank   | NULL = activo; fecha = eliminado     |

### Métodos

| Método          | Retorno          | Descripción                                     |
| --------------- | ---------------- | ----------------------------------------------- |
| `soft_delete()` | `void`           | Setea `deleted_at` a `timezone.now()`           |
| `restore()`     | `void`           | Setea `deleted_at` a `None` (restaura)          |
| `is_deleted`    | `bool` (prop)    | `True` si `deleted_at` no es `None`             |

---
## SoftDeleteManager

### Descripción
`SoftDeleteManager` es el manager por defecto asignado a `SoftDeleteModel.objects`.
Reemplaza el queryset base filtrando automáticamente `deleted_at IS NULL`, de modo que
todas las consultas estándar (`Model.objects.all()`, `filter()`, etc.) excluyen registros
eliminados lógicamente.

Para consultar también los registros eliminados se usa `Model.all_objects.all()`.

### Relación UML
```
SoftDeleteManager ◇── SoftDeleteModel (composición — manager del modelo)
```

### Diagrama UML
```
    ┌────────────────────────────┐
    │    SoftDeleteManager       │
    ├────────────────────────────┤
    │ + get_queryset(): QuerySet │
    └────────────────────────────┘
```

---
## User (Modelo de Usuario)

### Descripción
`User` es el modelo de usuario personalizado de Alke Wallet. Extiende tanto
`AbstractUser` de Django (para aprovechar el sistema de autenticación) como
`SoftDeleteModel` (para soft delete). El campo de autenticación es `email`
en lugar del `username` por defecto de Django.

Se ubica en `apps/accounts/models.py` y mapea la tabla `users` del esquema físico.

### Relación UML
```
User ──▷ AbstractUser   (Herencia — Django)
User ──▷ SoftDeleteModel (Herencia — mixin)
User ◆── UserManager     (composición — manager objects)
User ──o Account         (1 usuario → 0..* cuentas vía FK)
```

### Diagrama UML
```
    ┌─────────────────────────────────────┐
    │                User                 │
    ├─────────────────────────────────────┤
    │ + user_name : CharField(60)         │
    │ + email     : EmailField(100)       │
    │   <<unique>>                        │
    ├─────────────────────────────────────┤
    │ USERNAME_FIELD  = "email"           │
    │ REQUIRED_FIELDS = ["user_name"]     │
    ├─────────────────────────────────────┤
    │ + objects    : UserManager          │
    │ + all_objects: Manager              │
    ├─────────────────────────────────────┤
    │ + __str__() : str                   │
    │ + get_active_accounts() : QuerySet  │
    └────────────────┬────────────────────┘
                     │
          ┌──────────┴──────────┐
          │ hereda (múltiple)   │
          ▼                     ▼
    ┌───────────────┐   ┌───────────────────┐
    │ AbstractUser  │   │  SoftDeleteModel  │
    │  <<Django>>   │   │   <<abstracto>>   │
    └───────────────┘   └───────────────────┘
```

### Atributos Propios

| Atributo    | Tipo       | Opciones               | Descripción                  |
| ----------- | ---------- | ---------------------- | ---------------------------- |
| `user_name` | CharField  | max_length=60          | Nombre visible del usuario   |
| `email`     | EmailField | max_length=100, unique | Campo de autenticación       |

### Atributos Heredados (AbstractUser)

| Atributo      | Descripción                       |
| ------------- | --------------------------------- |
| `password`    | Contraseña (con hash)             |
| `is_staff`    | Acceso al panel de administración |
| `is_superuser`| Todos los permisos                |
| `is_active`   | Usuario activo                    |
| `date_joined` | Fecha de registro                 |

### Atributos Heredados (SoftDeleteModel)

| Atributo     | Tipo          | Descripción                      |
| ------------ | ------------- | -------------------------------- |
| `created_at` | DateTimeField | Timestamp de creación            |
| `updated_at` | DateTimeField | Timestamp de modificación        |
| `deleted_at` | DateTimeField | NULL = activo; fecha = eliminado |

---
## UserManager

### Descripción
`UserManager` es el manager personalizado para el modelo `User`. Hereda de
`BaseUserManager` de Django y reemplaza el queryset base para filtrar usuarios
activos (soft delete). Proporciona métodos para crear usuarios y superusuarios
usando `email` en lugar de `username`.

### Relación UML
```
UserManager ──▷ BaseUserManager (Herencia — Django)
UserManager ◇── User            (composición — manager objects)
```

### Diagrama UML
```
    ┌────────────────────────────────────────────────┐
    │                UserManager                     │
    ├────────────────────────────────────────────────┤
    │ + get_queryset() : QuerySet                    │
    │   (filtra deleted_at IS NULL)                  │
    │ + create_user(email, user_name, pwd) : User    │
    │ + create_superuser(email, user_name, pwd): User│
    └────────────────────────────────────────────────┘
                        ▲
                        │ hereda
                        │
        ┌────────────────────────────┐
        │    BaseUserManager         │
        │       <<Django>>           │
        └────────────────────────────┘
```

---
## Currency (Modelo de Moneda)

### Descripción
`Currency` representa las monedas disponibles en el sistema. Hereda de
`SoftDeleteModel`. Cada moneda tiene un nombre único y un símbolo ISO 4217 único.
Los datos iniciales se cargan con la fixture `currencies.json` (CLP, USD, EUR, CNY, CAD).

### Relación UML
```
Currency ──▷ SoftDeleteModel (Herencia — mixin)
Currency ──o Account         (1 moneda → 0..* cuentas vía FK)
```

### Diagrama UML
```
    ┌──────────────────────────────────────┐
    │              Currency                │
    ├──────────────────────────────────────┤
    │ + currency_name   : CharField(50)    │
    │   <<unique>>                         │
    │ + currency_symbol : CharField(3)     │
    │   <<unique>>                         │
    ├──────────────────────────────────────┤
    │ + __str__() : str                    │
    └──────────────────────────────────────┘
                    ▲
                    │ hereda
                    │
        ┌──────────────────────────┐
        │      SoftDeleteModel     │
        │       <<abstracto>>      │
        └──────────────────────────┘
```

### Atributos Propios

| Atributo          | Tipo      | Opciones              | Descripción         |
| ----------------- | --------- | --------------------- | ------------------- |
| `currency_name`   | CharField | max_length=50, unique | Nombre de la moneda |
| `currency_symbol` | CharField | max_length=3, unique  | Símbolo ISO 4217    |

---
## Account (Modelo de Cuenta)

### Descripción
`Account` representa la cuenta/billetera de un usuario en una moneda específica.
Hereda de `SoftDeleteModel`. Un usuario puede tener múltiples cuentas en distintas
monedas. El balance usa `DecimalField` para precisión monetaria exacta. Los depósitos
y retiros se realizan a través de los métodos de esta clase.

### Relación UML
```
Account ──▷ SoftDeleteModel  (Herencia — mixin)
Account ◆── User             (FK user — muchas cuentas por usuario)
Account ◆── Currency         (FK currency — una moneda por cuenta)
Account ──o Transaction      (0..1 como sender, 1 como receiver)
```

### Diagrama UML
```
    ┌──────────────────────────────────────┐
    │               Account                │
    ├──────────────────────────────────────┤
    │ + user     : FK → User               │
    │ + currency : FK → Currency           │
    │ + balance  : DecimalField(12,2)      │
    ├──────────────────────────────────────┤
    │ + __str__() : str                    │
    │ + deposit(amount) : void             │
    │ + withdraw(amount) : void            │
    └──────────────────────────────────────┘
```

### Atributos Propios

| Atributo   | Tipo         | Opciones                                   | Descripción            |
| ---------- | ------------ | ------------------------------------------ | ---------------------- |
| `user`     | ForeignKey   | → User, CASCADE, related=accounts          | Propietario            |
| `currency` | ForeignKey   | → Currency, PROTECT, related=accounts      | Moneda                 |
| `balance`  | DecimalField | max_digits=12, decimal_places=2, default=0 | Saldo                  |

### Métodos

| Método             | Retorno | Raises        | Descripción                             |
| ------------------ | ------- | ------------- | --------------------------------------- |
| `deposit(amount)`  | void    | ValueError    | Incrementa saldo (amount > 0)           |
| `withdraw(amount)` | void    | ValueError    | Decrementa saldo (0 < amount ≤ balance) |

---
## Transaction (Modelo de Transacción)

### Descripción
`Transaction` registra movimientos de dinero entre cuentas. Hereda de `SoftDeleteModel`.
Representa dos tipos de operaciones usando el mismo modelo:

- **Depósito externo**: `sender_account = NULL` → dinero entra desde fuera del sistema.
- **Transferencia**: `sender_account != NULL` → dinero se mueve entre cuentas de usuarios.

La propiedad `transaction_type` discrimina el tipo de operación.

### Relación UML
```
Transaction ──▷ SoftDeleteModel   (Herencia — mixin)
Transaction ◆── Account           (FK sender_account, nullable — 0..1)
Transaction ◆── Account           (FK receiver_account — 1)
```

### Diagrama UML
```
    ┌───────────────────────────────────────────────────┐
    │                    Transaction                    │
    ├───────────────────────────────────────────────────┤
    │ + sender_account  : FK → Account (NULL=True)      │
    │ + receiver_account: FK → Account                  │
    │ + amount          : DecimalField(12,2)            │
    │ + transaction_date: DateTimeField (auto_now_add)  │
    ├───────────────────────────────────────────────────┤
    │ + __str__() : str                                 │
    │ + transaction_type : str <<property>>             │
    │   → "deposito" | "transferencia"                  │
    └───────────────────────────────────────────────────┘
```

### Atributos Propios

| Atributo            | Tipo         | Opciones                              | Descripción                   |
| ------------------- | ------------ | ------------------------------------- | ----------------------------- |
| `sender_account`    | ForeignKey   | → Account, SET_NULL, null=True, blank | Cuenta origen (NULL=depósito) |
| `receiver_account`  | ForeignKey   | → Account, CASCADE                    | Cuenta destino                |
| `amount`            | DecimalField | max_digits=12, decimal_places=2       | Monto de la operación         |
| `transaction_date`  | DateTimeField| auto_now_add=True                     | Fecha/hora automática         |

### Propiedad

| Propiedad          | Retorno | Descripción                                             |
| ------------------ | ------- | ------------------------------------------------------- |
| `transaction_type` | str     | "deposito" si sender=None, "transferencia" en otro caso |

---
## RegisterForm

### Descripción
`RegisterForm` es el formulario de registro de nuevos usuarios. Hereda de
`UserCreationForm` de Django para aprovechar la validación de contraseñas.
Incluye los campos propios del modelo `User` personalizado: `email` y `user_name`.

### Relación UML
```
RegisterForm ──▷ UserCreationForm (Herencia — Django)
RegisterForm ───  User            (Meta.model = User)
```

### Diagrama UML
```
    ┌──────────────────────────────────────────────┐
    │               RegisterForm                   │
    ├──────────────────────────────────────────────┤
    │ + email     : EmailField                     │
    │ + user_name : CharField(60)                  │
    ├──────────────────────────────────────────────┤
    │ Meta.model  = User                           │
    │ Meta.fields = (user_name, email,             │
    │                password1, password2)         │
    └──────────────────────────────────────────────┘
                    ▲
                    │ hereda
                    │
        ┌──────────────────────────┐
        │    UserCreationForm      │
        │       <<Django>>         │
        └──────────────────────────┘
```

---
## LoginForm

### Descripción
`LoginForm` hereda de `AuthenticationForm` de Django con estilos Bootstrap aplicados
a sus campos. Usa `email` como campo de autenticación (acorde con `USERNAME_FIELD = "email"`).

### Relación UML
```
LoginForm ──▷ AuthenticationForm (Herencia — Django)
```

### Diagrama UML
```
    ┌──────────────────────────┐
    │        LoginForm         │
    ├──────────────────────────┤
    │ + username : EmailField  │
    │ + password : CharField   │
    └──────────────────────────┘
                ▲
                │ hereda
                │
    ┌──────────────────────────┐
    │   AuthenticationForm     │
    │       <<Django>>         │
    └──────────────────────────┘
```

---
## DepositForm

### Descripción
`DepositForm` valida los datos de entrada para realizar un depósito en una cuenta.
Hereda directamente de `forms.Form` (no de un ModelForm). Valida que el monto sea
un valor decimal positivo (mínimo 0.01).

### Relación UML
```
DepositForm ──▷ forms.Form (Herencia — Django)
```

### Diagrama UML
```
    ┌──────────────────────────────────────┐
    │           DepositForm                │
    ├──────────────────────────────────────┤
    │ + amount : DecimalField              │
    │   min_value=0.01, max_digits=12      │
    │   decimal_places=2                   │
    ├──────────────────────────────────────┤
    │ + clean_amount() : Decimal           │
    └──────────────────────────────────────┘
                    ▲
                    │ hereda
                    │
        ┌──────────────────────────┐
        │       forms.Form         │
        │       <<Django>>         │
        └──────────────────────────┘
```

### Campos

| Campo    | Tipo         | Validación                 | Descripción          |
| -------- | ------------ | -------------------------- | -------------------- |
| `amount` | DecimalField | min=0.01, max_digits=12, dec=2 | Monto a depositar |

---
## SendMoneyForm

### Descripción
`SendMoneyForm` valida los datos para transferir dinero a otro usuario. Hereda de
`forms.Form`. Incluye el monto (obligatorio) y un mensaje opcional para describir
la transferencia. El campo `message` no se persiste en el modelo `Transaction`,
su uso es informativo en la vista.

### Relación UML
```
SendMoneyForm ──▷ forms.Form (Herencia — Django)
```

### Diagrama UML
```
    ┌──────────────────────────────────────┐
    │          SendMoneyForm               │
    ├──────────────────────────────────────┤
    │ + amount  : DecimalField             │
    │   min_value=0.01, max_digits=12      │
    │ + message : CharField(255)           │
    │   required=False                     │
    ├──────────────────────────────────────┤
    │ + clean_amount() : Decimal           │
    └──────────────────────────────────────┘
                    ▲
                    │ hereda
                    │
        ┌──────────────────────────┐
        │       forms.Form         │
        │       <<Django>>         │
        └──────────────────────────┘
```

### Campos

| Campo     | Tipo         | Validación                     | Descripción                  |
| --------- | ------------ | ------------------------------ | ---------------------------- |
| `amount`  | DecimalField | min=0.01, max_digits=12, dec=2 | Monto a transferir           |
| `message` | CharField    | max_length=255, required=False | Descripción (opcional)       |

