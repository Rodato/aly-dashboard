# CLAUDE.md — Dashboard AlyBot

## Correr en local
```bash
python3 -m streamlit run app.py
```
`streamlit` no está en el PATH — siempre usar `python3 -m streamlit`.

---

## Proyecto
Dashboard operativo privado para **Apapáchar** (chatbot WhatsApp RAG, crianza 0-5 años, Fundación Apapacho).

---

## Stack
- **Streamlit ≥ 1.50** — UI con `st.navigation` multi-página
- **Supabase** (PostgreSQL) — conexión via `psycopg2` con `RealDictCursor`
- **Plotly** — gráficas via fábrica centralizada en `components/charts.py`
- **python-dotenv** — `.env` cargado en `app.py`

---

## Estructura de archivos
```
Aly_dashboard/
├── .env                        # DATABASE_URL
├── app.py                      # Entry point — st.navigation, CSS, render_sidebar()
├── pages/
│   ├── overview.py             # Inicio: KPIs+delta, growth chart, activity heatmap
│   ├── usuarios.py             # Demografía: choropleth, donut género, bar regiones, barras horarias
│   ├── conversaciones.py       # Keywords (parsea conversations_data.keywords) + resúmenes
│   ├── alertas.py              # Solo flags 🔴/🟠 (HIGH-/MEDIUM-); export Excel con transcripción; toggle revisado
│   └── leaderboard.py          # Top usuarios: podio, bar chart top 10, tabla top 20 con columna Flags 🚩
├── components/
│   ├── filters.py              # Sidebar: logo, lang toggle, date pickers+presets 7d/30d, export Excel interacciones
│   ├── kpi_row.py              # Fila de KPI cards con delta % vs período anterior
│   └── charts.py               # Fábrica Plotly: bar_h, donut, choropleth, bar_v
├── utils/
│   ├── db.py                   # Todas las queries SQL
│   ├── i18n.py                 # Traducciones ES/EN via t("key")
│   └── styles.py               # CSS global + COLORS dict + section_label() + page_header()
└── requirements.txt
```

---

## Tablas Supabase
| Tabla | Columnas clave |
|---|---|
| `public.users_interactions` | `conversation_id`, `client_number`, `role`, `message`, `timestamp`, `status`, `created_at` |
| `public.users_data` | `number`, `name`, `country`, `gender`, `region`, `email`, `created_at` |
| `public.conversations_data` | `conversation_id`, `user_number`, `conversation_date`, `summary`, `keywords`, `flags`, `session` |
| `vector_aly.rag_embeddings` | `project`, `document_name`, `topics`, `entities`, `key_phrases`, `chunk_index` |

---

## Queries en db.py
- `get_user_kpis(from, to)` → dict n_users, n_sessions
- `get_messages_count(from, to)` → int
- `get_hourly_distribution(from, to)` → df hour/messages
- `get_users_by_country/gender/region(from, to)` → df
- `get_daily_activity(from, to)` → df day/messages/users
- `get_activity_heatmap(from, to)` → df dow/hour/messages
- `get_conversation_metrics(from, to)` → dict métricas agregadas
- `get_kpi_deltas(from, to)` → dict deltas fraccionales vs período anterior
- `get_conversations_data(from, to)` → df completo de conversations_data
- `get_summaries(from, to, limit)` → df resúmenes recientes
- `get_flags_data(from, to)` → df conversaciones con flags (todas, sin filtrar severidad)
- `get_flag_counts_by_user(from, to)` → df user_number/n_flags (solo HIGH-/MEDIUM-)
- `get_leaderboard(from, to, limit)` → df top usuarios por mensajes totales
- `get_interactions_export(from, to)` → df para Excel export de interacciones
- `get_messages_by_conversation_ids(conv_ids)` → df mensajes para lista de conversation_ids
- `get_user_conversations(user_number, from, to)` → df conversaciones de un usuario (drill-down)
- `get_user_messages(user_number, from, to)` → df mensajes de un usuario (drill-down)

---

## Convenciones obligatorias
- **SQL**: siempre parametrizado con `%s`. Nunca f-strings con datos externos. `_date_filter()` construye el WHERE.
- **Filtros globales**: en `st.session_state` (`filter_from`, `filter_to`). Inicializados en `components/filters.py`. Páginas los leen con `get_filters()`.
- **Widgets Streamlit**: si un widget usa `key=`, NO pasar también `value=` — Streamlit lanza warning. Usar session_state para el valor inicial.
- **Texto**: todo via `t("key")` de `utils/i18n.py`. Agregar claves nuevas en ambos idiomas.
- **CSS**: inyectado con `st.html(css)` en `utils/styles.inject()`. No usar `st.markdown(unsafe_allow_html=True)` para CSS.
- **Colores**: siempre desde el dict `COLORS` de `utils/styles.py`. No hardcodear hex.
- **Números de teléfono**: enmascarar en la UI (primeros 4 dígitos + `****` + últimos 2). El Excel de alertas exporta el número sin mask intencionalmente para el equipo de respuesta.

---

## Clasificación de flags
El campo `flags` en `conversations_data` es un string CSV con múltiples flags por conversación, cada una con prefijo de severidad:
- `HIGH-<razón>` → 🔴 rojo (crítico)
- `MEDIUM-<razón>` → 🟠 naranja (advertencia)
- `LOW-<razón>` → ignorado en UI (no se muestra)

La lógica de clasificación vive en `_classify_flag()` en `pages/alertas.py`. El leaderboard usa la misma lógica en Python (no SQL) para contar flags por usuario.

**Si el bot cambia el formato de estos campos, actualizar `_classify_flag()` en `alertas.py` y la lógica en `leaderboard.py`.**

---

## Estilo visual
- **Fuentes**: Oswald (títulos, valores KPI) · Open Sans (todo lo demás) — Google Fonts
- **Sidebar**: oscura `#0C1214`
- **Cards / fondo contenedores**: blanco `#FFFFFF`
- **Fondo app**: `#F0F2F5`
- **Accent principal**: `#0273e5`
- **Positivo/negativo**: `#22C55E` / `#F15B22`

---

## Proyecto Complementario: Aly_Apapachar

**Ubicación**: `/Users/daniel/Desktop/Dev/Aly_Apapachar/`

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
| `public.conversations_data` | Conversation Closer (al cerrar sesión) |
| `vector_aly.rag_embeddings` | scripts de ingest |

---

## Deployment
- **Local**: `python3 -m streamlit run app.py`
- **Producción**: Streamlit Cloud (share.streamlit.io) — secret necesario: `DATABASE_URL`
- Auto-redeploy al hacer push a `main`
