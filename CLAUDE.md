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
│   ├── alertas.py              # Flags (conversations_data.flags) con clasificación 🔴/🟠
│   └── leaderboard.py          # Top usuarios: podio, bar chart top 10, tabla completa top 20
├── components/
│   ├── filters.py              # Sidebar: logo, lang toggle, date pickers+presets 7d/30d, export Excel
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
- `get_flags_data(from, to)` → df conversaciones con flags
- `get_leaderboard(from, to, limit)` → df top usuarios por mensajes totales
- `get_interactions_export(from, to)` → df para Excel export

---

## Convenciones obligatorias
- **SQL**: siempre parametrizado con `%s`. Nunca f-strings con datos externos. `_date_filter()` construye el WHERE.
- **Filtros globales**: en `st.session_state` (`filter_from`, `filter_to`). Inicializados en `components/filters.py`. Páginas los leen con `get_filters()`.
- **Widgets Streamlit**: si un widget usa `key=`, NO pasar también `value=` — Streamlit lanza warning. Usar session_state para el valor inicial.
- **Texto**: todo via `t("key")` de `utils/i18n.py`. Agregar claves nuevas en ambos idiomas.
- **CSS**: inyectado con `st.html(css)` en `utils/styles.inject()`. No usar `st.markdown(unsafe_allow_html=True)` para CSS.
- **Colores**: siempre desde el dict `COLORS` de `utils/styles.py`. No hardcodear hex.
- **Números de teléfono**: enmascarar en la UI (primeros 4 dígitos + `****` + últimos 2).

---

## Estilo visual
- **Fuentes**: Oswald (títulos, valores KPI) · Open Sans (todo lo demás) — Google Fonts
- **Sidebar**: oscura `#0C1214`
- **Cards / fondo contenedores**: blanco `#FFFFFF`
- **Fondo app**: `#F0F2F5`
- **Accent principal**: `#0273e5`
- **Positivo/negativo**: `#22C55E` / `#F15B22`

---

## Deployment
- **Local**: `python3 -m streamlit run app.py`
- **Producción**: Streamlit Cloud (share.streamlit.io) — secret necesario: `DATABASE_URL`
- Auto-redeploy al hacer push a `main`
