# CLAUDE.md — Dashboard Aly

## Documentación (Obsidian)
Notas en: `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Documentición codigo/Aly Bot (Equimundo)/`
Actualizar cuando cambien: arquitectura, stack, esquema Supabase, páginas/componentes, flujo de datos bot→dashboard.
No actualizar por: bugfixes menores, ajustes de UI, cambios de copy.

## Correr en local
```bash
python3 -m streamlit run app.py
```
`streamlit` no está en el PATH — siempre usar `python3 -m streamlit`.

---

## Proyecto
Dashboard operativo privado para **Apapáchar** (chatbot WhatsApp RAG, crianza 0-5 años, Fundación Apapacho). Marca visible: **Aly**.

**Multi-bot — alcance del dashboard:** la DB de Supabase es compartida. Las 3 tablas (`users_interactions`, `users_data`, `conversations_data`) tienen columna `bot_id` (type `text`, `NOT NULL`, default `''`). El bot escribe `'apapachar'` o `'demo'` según `BOT_ID` env var.

El dashboard **detecta automáticamente** los `bot_id` disponibles en la DB (`utils/db.py:get_available_bot_ids()`) y muestra un **selector en el sidebar** (arriba de los filtros de fecha). El usuario elige qué bot ver; todas las queries filtran por el `bot_id` seleccionado. El valor seleccionado vive en `st.session_state["selected_bot"]` y se pasa via `get_filters()["bot_id"]`.

**Estado actual (2026-06-15)**: hay **autenticación con roles** (ver sección *Autenticación y roles*). El selector de bot se filtra por el rol del usuario logueado: `admin` ve todos los bots; `apapachar` queda bloqueado al bot `apapachar` (sin selector, chip fijo).

---

## Autenticación y roles
Login usuario/contraseña con **`streamlit-authenticator` (0.4.x)**. La puerta vive en `utils/auth.py:require_login()`, llamada en `app.py` **antes** de la nav y las páginas: si no hay sesión válida renderiza la pantalla de login (logo Aly + form) y hace `st.stop()`. La sesión persiste vía cookie firmada (no re-login en cada rerun).

**Credenciales y roles viven en `st.secrets`** (`.streamlit/secrets.toml` en local — **gitignored**; secrets manager en Streamlit Cloud). Plantilla commiteada: `.streamlit/secrets.toml.example`. Estructura: `[cookie]`, `[credentials.usernames.<user>]` (con `password` = **hash bcrypt**, `roles = ["..."]`) y `[roles]` que mapea rol → lista de `bot_id` permitidos (`"*"` = todos).

**Generar un hash bcrypt** para una contraseña nueva:
```bash
python3 -c "import bcrypt; print(bcrypt.hashpw(b'PASSWORD', bcrypt.gensalt()).decode())"
```

**Flujo rol → bots**: `require_login()` deja en session_state `auth_role`, `auth_allowed_bots` (None = todos, o lista de bot_ids), `auth_name`, `_authenticator`. `components/filters.py` lee `auth_allowed_bots` y: si es None muestra el selector con todos los bots; si es lista de 1 oculta el selector y fija el bot (chip `.bot-locked`); si la selección actual no es válida para el rol, la resetea. El logout (`authenticator.logout`) y el "Conectado como" se renderizan en el footer del sidebar.

**Roles actuales**: `admin` → `["*"]` (todos los bots); `apapachar` → `["apapachar"]` (solo datos de Colombia).

**Agregar un usuario/rol nuevo**: añadir `[credentials.usernames.<user>]` (hash + `roles`) y, si es un rol nuevo, una entrada en `[roles]`. Si es un rol nuevo, agregar también la clave i18n `role_<rol>` en `utils/i18n.py`. Sin migración de DB.

---

## Stack
- **Streamlit ≥ 1.50** — UI con `st.navigation(position="hidden")` + nav custom en sidebar
- **Supabase** (PostgreSQL) — conexión via `psycopg2` con `RealDictCursor`
- **Plotly** — gráficas via fábrica centralizada en `components/charts.py`
- **python-dotenv** — `.env` cargado en `app.py`

---

## Estructura de archivos
```
Aly_dashboard/
├── .env                        # DATABASE_URL
├── .streamlit/
│   ├── config.toml             # Tema Streamlit
│   ├── secrets.toml            # Auth: credenciales + roles (GITIGNORED — no commitear)
│   └── secrets.toml.example    # Plantilla commiteada del secrets.toml
├── app.py                      # Entry point — auth gate (require_login), st.navigation (position="hidden"), CSS, render_sidebar() + render_topbar()
├── pages/
│   ├── overview.py             # Inicio: hero banner, 4 KPIs con sparkline + caption explicativo, growth chart + stat_list (peak hour/day, grid 2:1), heatmap bloques. La gráfica de actividad rellena días sin datos con 0, fija el eje X al rango y desactiva el zoom de Plotly (ver Convenciones)
│   ├── usuarios.py             # Demografía: 3 KPIs (users, regiones, msg/usuario), layout 2:1 — choropleth Colombia (33 deptos) a la izquierda, cobertura + ranking top 10 a la derecha
│   ├── conversaciones.py       # Keywords + resúmenes (no está en nav, en standby)
│   ├── alertas.py              # Flags 🔴/🟠 (HIGH-/MEDIUM-), export Excel con transcripción, "marcar revisado" persistido en Supabase (reviewed_at)
│   └── leaderboard.py          # Top usuarios: podio, bar top 10, tabla top 20 con Flags 🚩, drill-down con tabs (header muestra teléfono completo del usuario)
├── components/
│   ├── filters.py              # render_sidebar() (logo Aly, nav custom Material icons, bot selector role-aware, date pickers + presets 7d/30d con on_click callbacks, "conectado como" + logout) + render_topbar() (selector de idioma ES/EN arriba a la derecha). get_filters() lee session_state. Sin export — descarga vive en Alertas
│   ├── kpi_row.py              # KPI cards HTML custom: accent bar + icon + sparkline SVG + delta pill. ICONS dict reutilizable
│   └── charts.py               # Fábrica Plotly: bar_h, donut, bar_v, choropleth (silueta flat + dots), choropleth_colombia (departamentos con aliases)
├── data/
│   └── colombia_departments.geojson  # GeoJSON bundled (33 deptos, featureidkey="properties.NOMBRE_DPT")
├── utils/
│   ├── auth.py                 # require_login(): login streamlit-authenticator + resolución rol→bots + logout
│   ├── db.py                   # Todas las queries SQL
│   ├── i18n.py                 # Traducciones ES/EN via t("key")
│   ├── styles.py               # CSS global + COLORS dict + helpers: page_header, hero_banner, card_header, stat_list, arc_row, section_label
│   └── translate.py            # Traducción de keywords (usada en leaderboard)
└── requirements.txt
```

---

## Navegación
`st.navigation(pages, position="hidden")` oculta la nav nativa; la real se renderiza en `_render_nav()` (components/filters.py) con `st.page_link` + Material Symbols (`:material/dashboard:`, `:material/group:`, `:material/warning:`, `:material/emoji_events:`) agrupados en secciones **ANÁLISIS** (Inicio, Usuarios) y **OPERACIÓN** (Alertas, Leaderboard). La página `conversaciones.py` existe pero no está en `NAV_ITEMS` ni en `app.py:pages`.

**Selector de idioma**: vive en `render_topbar()` (no en el sidebar) — un `st.segmented_control(["ES","EN"], key="lang_seg")` alineado a la derecha del área principal, renderizado en `app.py` antes de `pg.run()` para que aparezca en todas las páginas. Su `on_change` escribe `st.session_state.lang`. CSS: `.topbar-lang` + override compacto de `[data-testid="stSegmentedControl"]` en `utils/styles.py`.

---

## Tablas Supabase
| Tabla | Columnas clave |
|---|---|
| `public.users_interactions` | `conversation_id`, `client_number`, `role`, `message`, `timestamp`, `status`, `created_at` |
| `public.users_data` | `number`, `name`, `country`, `gender`, `region`, `email`, `created_at` |
| `public.conversations_data` | `conversation_id`, `user_number`, `conversation_date`, `summary`, `keywords`, `flags`, `session`, `reviewed_at` (TIMESTAMPTZ — null si pendiente) |
| `vector_aly.rag_embeddings` | `project`, `document_name`, `topics`, `entities`, `key_phrases`, `chunk_index` |

---

## Queries en db.py
Todas las queries de tiempo convierten a **GMT-5 (`America/Bogota`)** vía `AT TIME ZONE` antes de filtrar/extraer hora. Constante `TZ` arriba del módulo.

`_date_filter()` además excluye **siempre** cuentas de testing/eval que vienen del repo hermano `aly-evals` (benchmarks, smoke tests, verify, debug). Las listas viven al inicio de `utils/db.py`: `_TEST_CLIENT_NUMBERS`, `_TEST_CLIENT_LIKE`, `_TEST_CONV_LIKE`. Si aly-evals agrega un nuevo prefijo sentinel, sumarlo a la tupla correspondiente. Queries sobre `conversations_data` pasan `client_col="user_number"`; queries con alias pasan nombres calificados (`client_col="ui.client_number"`). Los drill-downs por usuario explícito apagan el filtro con `client_col=None, conv_col=None`.

- `fetch_df(query, params)` → DataFrame (lecturas)
- `execute(query, params)` → rowcount (escrituras INSERT/UPDATE/DELETE)
- `get_user_kpis(from, to)` → dict n_users, n_sessions
- `get_messages_count(from, to)` → int
- `get_hourly_distribution(from, to)` → df hour/messages (hora en GMT-5; no se usa actualmente en UI — disponible)
- `get_users_by_country/gender/region(from, to)` → df
- `get_daily_activity(from, to)` → df day/messages/users/**sessions** (day en GMT-5; sessions se usa para sparklines de Inicio)
- `get_activity_heatmap(from, to)` → df dow/hour/messages (en GMT-5)
- `get_conversation_metrics(from, to)` → dict métricas agregadas (incluye `avg_msg_per_user`)
- `get_kpi_deltas(from, to)` → dict deltas fraccionales vs período anterior
- `get_conversations_data(from, to)` → df completo de conversations_data
- `get_summaries(from, to, limit)` → df resúmenes recientes
- `get_flags_data(from, to)` → df conversaciones con flags + `reviewed_at` (en GMT-5)
- `mark_flag_reviewed(conv_id)` → UPDATE … SET reviewed_at = NOW()
- `unmark_flag_reviewed(conv_id)` → UPDATE … SET reviewed_at = NULL
- `get_flag_counts_by_user(from, to)` → df user_number/n_flags (solo HIGH-/MEDIUM-)
- `get_leaderboard(from, to, limit)` → df top usuarios (last_seen / days_active en GMT-5)
- `get_interactions_export(from, to)` → df para Excel export de interacciones (queda disponible aunque ya no se exponga en sidebar)
- `get_messages_by_conversation_ids(conv_ids)` → df mensajes para lista de conversation_ids
- `get_user_conversations(user_number, from, to)` → df conversaciones de un usuario (drill-down)
- `get_user_messages(user_number, from, to)` → df mensajes de un usuario (drill-down)

---

## Componentes reutilizables (utils/styles.py)
- `page_header(title, subtitle="", show_period=True)` — H1 + subtítulo + chip de período (auto desde session_state).
- `hero_banner(headline_html, status_text, status_kind, meta_label, meta_value)` — banner gradient con status pill (`ok`/`warn`/`crit`) y número destacado a la derecha. Usa `<b>` dentro del headline para números grandes.
- `card_header(title, subtitle="", icon_svg="", right_text="")` — header estándar sobre charts/tablas. Reemplaza al viejo `section_label` (que existe pero está legacy).
- `stat_list(items=[{label, value}])` — card vertical compacto tipo sidebar stats.
- `arc_row(items=[{label, pct, value?, accent?}])` — fila de gauges SVG 3/4 (0-100%), label arriba, value dentro del arco.
- `section_label(text)` — legacy, evitar en páginas nuevas.

## KPI cards (components/kpi_row.py)
`render(metrics: list[dict])`. Cada dict:
- `label`, `value`, `delta` (fracción o None), `delta_label`, `prefix`, `suffix`
- `accent`: color key de COLORS (`accent` | `navy` | `positive` | `yellow` | `red`) — pinta la barra izquierda y los dots del sparkline
- `icon`: key de `kpi_row.ICONS` (`users`, `message`, `send`, `chart`, `alert-triangle`, `alert-circle`, `flag`, `activity`)
- `spark`: lista de valores para sparkline SVG inline (opcional)
- `caption`: oración corta explicativa bajo el valor (opcional) — clase `.kpi-card__caption`. En Inicio cada KPI la usa para autoexplicarse (ej. "Personas que interactuaron con Aly").

---

## Convenciones obligatorias
- **SQL**: siempre parametrizado con `%s`. Nunca f-strings con datos externos. `_date_filter()` construye el WHERE.
- **Zona horaria**: la DB guarda timestamptz en UTC, pero la UI opera en **GMT-5 (`America/Bogota`)**. Toda query nueva que extraiga hora/día o filtre por fecha debe convertir con `AT TIME ZONE '{TZ}'` (constante en `utils/db.py`). El "today" del sidebar también se calcula con `ZoneInfo("America/Bogota")`.
- **Filtros globales**: en `st.session_state` (`filter_from`, `filter_to`). Inicializados en `components/filters.py`. Páginas los leen con `get_filters()` (que devuelve `date_to` **exclusivo** = fecha elegida + 1 día).
- **Gráficas de series temporales**: las queries (`get_daily_activity`, etc.) solo devuelven días **con** datos. Para que el filtro de fechas se vea respetado, rellenar los días faltantes con 0 (reindex sobre `pd.date_range(date_from, date_to)`), fijar el eje X con `fig.update_xaxes(range=[...], fixedrange=True)` y desactivar el modebar (`config={"displayModeBar": False}`). Si hay menos días con datos que el span, mostrar `t("sparse_data_note")`. Patrón vivo en `overview.py` (actividad diaria). Evita que un rango con datos escasos parezca un filtro roto.
- **Widgets Streamlit**: si un widget usa `key=`, NO pasar también `value=` — Streamlit lanza warning. Usar session_state para valor inicial. Para presets que mutan widget keys (ej. `7d`/`30d`), usar `on_click` callbacks — asignar a `st.session_state[key]` después de renderizar el widget se ignora silenciosamente.
- **Texto**: todo via `t("key")` de `utils/i18n.py`. Agregar claves nuevas en ambos idiomas.
- **CSS**: inyectado con `st.html(css)` en `utils/styles.inject()`. HTML de componentes sí usa `st.markdown(unsafe_allow_html=True)` (ver `hero_banner`, `card_header`, `arc_row`, `kpi_row`).
- **Colores**: siempre desde el dict `COLORS` de `utils/styles.py`. No hardcodear hex.
- **Números de teléfono**: enmascarar en la UI (primeros 4 dígitos + `****` + últimos 2). El Excel de alertas exporta el número sin mask intencionalmente para el equipo de respuesta.
- **Íconos del sidebar**: override CSS para que las ligatures de Material Symbols no hereden `Open Sans` del selector global `*` del sidebar (ver `utils/styles.py`).
- **Estado compartido entre usuarios**: persistir en Supabase, no en `st.session_state` (que es por sesión de browser). Ej.: `reviewed_at` de las flags vive en `conversations_data`, no en memoria.
- **Filtrado de cuentas test**: toda query nueva sobre `users_interactions/conversations_data` debe pasar por `_date_filter()` para heredar el filtro de aly-evals automáticamente. No bypassear con `fetch_df` directo sin pensar en qué datos estás trayendo.

---

## Clasificación de flags
El campo `flags` en `conversations_data` es un string CSV con múltiples flags por conversación, cada una con prefijo de severidad:
- `HIGH-<razón>` → 🔴 rojo (crítico)
- `MEDIUM-<razón>` → 🟠 naranja (advertencia)
- `LOW-<razón>` → ignorado en UI (no se muestra)

La lógica de clasificación vive en `_classify_flag()` en `pages/alertas.py`. También se replica en `pages/overview.py` (para el status del hero banner) y `pages/leaderboard.py` (para contar flags por usuario).

**Si el bot cambia el formato de estos campos, actualizar `_classify_flag()` en los 3 archivos.**

---

## Estilo visual
- **Fuentes**: Oswald (títulos, valores KPI, hero number) · Open Sans (body, labels, captions) · Material Symbols Rounded (íconos de nav) — Google Fonts
- **Sidebar**: claro `#FFFFFF` con borde gris, logo con cuadrado gradient (azul→navy) + wordmark "Aly"
- **Cards / fondo contenedores**: blanco `#FFFFFF`
- **Fondo app**: `#F7F8FA` (cool gray, más premium que el antiguo `#F0F2F5`)
- **Accent principal**: `#0273e5` · **Navy**: `#110079` · **Amarillo**: `#FFCF24` · **Naranja**: `#F15B22`
- **Positivo/negativo**: `#22C55E` / `#F15B22`
- **Heatmap**: `go.Heatmap` con `xgap=3, ygap=3` para bloques discretos tipo GitHub contributions; paleta gray→blue→accent.
- **Mapa de países**: `choropleth()` en charts.py renderiza **scattergeo silueta plana** — land `#D1D5DB`, sin bordes de países/costas, dots accent blue con halo soft bajo cada dot. **No se usa en Usuarios actualmente** (se reemplazó por el mapa de Colombia) pero la función queda disponible.
- **Mapa de Colombia**: `choropleth_colombia()` en charts.py — `go.Choropleth` con GeoJSON local (`data/colombia_departments.geojson`). Siempre renderiza los 33 departamentos (deptos sin datos en gris `#E5E7EB`); rampa `#DBEAFE→#3B82F6→accent` para deptos con usuarios. `showscale=False` (la cobertura ya está en el panel lateral). Aliases para normalizar variantes de input: `bogota`→`SANTAFE DE BOGOTA D.C`, `san andres`→`ARCHIPIELAGO ...`, `guajira`→`LA GUAJIRA`, `valle`→`VALLE DEL CAUCA`. Las regiones que no matchean ningún departamento se listan como caption bajo el mapa.

---

## Proyecto Complementario: Aly_Apapachar

**Ubicación**: `/Users/daniel/Documents/Dev/Aly_Apapachar/`

Aly_Apapachar es el bot WhatsApp (LangGraph + MongoDB + Twilio) que **genera los datos** que este dashboard visualiza.

### Flujo de datos
```
Aly_Apapachar (bot) → Conversation Closer → Supabase → este dashboard
```

### Contrato de datos
- `keywords`: string CSV — se parsea con `split(",")` en `conversaciones.py`
- `flags`: string CSV con prefijos `HIGH-` / `MEDIUM-` / `LOW-` por flag, múltiples flags por conversación
- `summary`: texto libre en el idioma del facilitador

### Quién escribe cada tabla
| Tabla | Escrita por |
|---|---|
| `public.users_interactions` | `bot.py` (cada mensaje) |
| `public.users_data` | `onboarding_agent.py` (registro nuevo usuario) |
| `public.conversations_data` | Conversation Closer escribe la fila inicial. El **dashboard** escribe `reviewed_at` cuando el equipo marca la flag como revisada |
| `vector_aly.rag_embeddings` | scripts de ingest |

### Otros escritores (ruido conocido)
`aly-evals` (repo hermano en `~/Documents/Dev/aly-evals/`) corre benchmarks contra el bot y termina escribiendo cientos de filas sentinel (`client_number IN ('eval','verify','smoke',…)`, `conversation_id LIKE 'eval-%' / 'verify-%' / 'debug-%' / …`). El filtro en `_date_filter()` las excluye automáticamente del dashboard. Antes del filtro (commit `d981c15`, 2026-05-27), `eval` solo aportaba 458 conversaciones / 918 mensajes.

---

## Deployment
- **Local**: `python3 -m streamlit run app.py`
- **Producción**: Streamlit Cloud (share.streamlit.io) — secret necesario: `DATABASE_URL`
- **URL**: https://aly-dashboard-pejmrmpdvh8wqefx2ibnzj.streamlit.app/
- Auto-redeploy al hacer push a `main`
- **Gotcha**: al agregar un símbolo nuevo a un módulo ya importado (ej. una función nueva en `components/filters.py`), el hot-reload puede fallar con `ImportError` por caché de `sys.modules`. Solución: **Reboot app** desde Manage app en Streamlit Cloud (no requiere cambio de código).
