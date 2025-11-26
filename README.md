# 💳 Alke Wallet - Billetera Digital

## Demo
**Accede a la demo aquí:** https://lmakr8.github.io/alke-wallet/

---

## Credenciales de Acceso
Para acceder a la aplicación, utiliza las siguientes credenciales:

```
Email:    usuario@ejemplo.com
Password: 12345
```

---

## Descripción del Proyecto
**Alke Wallet** es una aplicación web de billetera digital desarrollada como proyecto del **Módulo 2** del programa **Fullstack Python - Talento Digital 2025**. Esta solución simula una plataforma fintech completa que permite gestionar finanzas personales con una interfaz moderna, minimalista, responsive y funcional en el lado del cliente.

---

## Tecnologías Utilizadas

| Tecnología           | Versión | Propósito                                              |
| -------------------- | ------- | ------------------------------------------------------ |
| **HTML5**            | -       | Estructura semántica de las páginas                    |
| **CSS3**             | -       | Estilos personalizados con variables CSS y animaciones |
| **Bootstrap**        | 5.3.2   | Framework CSS para diseño responsive                   |
| **Bootstrap Icons**  | 1.11.1  | Iconografía vectorial                                  |
| **JavaScript**       | ES6+    | Lógica de negocio y manipulación del DOM               |
| **jQuery**           | 3.7.1   | Simplificación de operaciones DOM y eventos            |
| **LocalStorage API** | -       | Persistencia de datos del lado del cliente             |

---

## Estructura del Proyecto
El proyecto está organizado de la siguiente manera:

```
alke-wallet/
│
├── index.html                  # Página de bienvenida (Landing page)
├── README.md                   # Documentación del proyecto
│
├── pages/                      # Páginas de la aplicación
│   ├── login.html              # Pantalla de autenticación
│   ├── menu.html               # Dashboard principal
│   ├── deposit.html            # Módulo de depósitos
│   ├── sendMoney.html          # Módulo de transferencias y gestión de contactos
│   └── transactions.html       # Historial de movimientos
│
└── src/                        # Recursos del proyecto
    ├── css/
    │   └── style.css           # Estilos personalizados (variables CSS, animaciones)
    │
    └── js/                     # Scripts de JavaScript
        ├── index.js            # Lógica de la landing page
        ├── login.js            # Lógica de autenticación
        ├── menu.js             # Dashboard y navegación
        ├── deposit.js          # Gestión de depósitos
        ├── sendMoney.js        # Transferencias y CRUD de contactos
        └── transactions.js     # Historial, filtros y paginación
```

---

## Ramas del Proyecto
El proyecto utiliza las siguientes ramas:

| Rama                   | Descripción                                  | Estado      |
| ---------------------- | -------------------------------------------- | ----------- |
| `main`                 | Rama principal de producción                 | Activa      |
| `feature/login`        | Sistema de autenticación y validación        | Mergeada    |
| `feature/deposits`     | Módulo de depósitos y actualización de saldo | Mergeada    |
| `feature/transactions` | Historial, filtros y paginación              | Mergeada    |


### Convenciones de Commits
El proyecto sigue las convenciones de commits semánticos:

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bugs
- `style:` Cambios de estilos (CSS)
- `refactor:` Refactorización de código
- `docs:` Actualización de documentación

---

## Autor
**Desarrollado por**: Leandro Marchant  
**Programa**: Fullstack Python - Talento Digital 2025  
**Módulo**: 2 - Desarrollo Front-end  
**Año**: 2025
