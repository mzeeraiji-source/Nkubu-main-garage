# Nkubu-main-garage
A automotive workshop website with  e-commerse store 
A full-stack, AI-native local garage ecosystem. 30+ pages. Vercel-hosted. Supabase + Neon dual-database architecture. Python brain + server. Claude Extensions for intelligent automation.
This README is the single source of truth — the AI command center.                                                 |

┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACE LAYER                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐ │
│  │   Garage     │  │   Shopify    │  │   Booking    │  │   AI Assistant │ │
│  │   Website    │  │   Storefront │  │   Portal     │  │   (Claude)     │ │
│  │  (15+ pages) │  │  (10+ pages) │  │  (5+ pages)  │  │  (Chat + Ext)  │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────────┘ │
│                              ▲                                              │
│                              │                                              │
│                              ▼                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                        VERCEL EDGE NETWORK                            │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │   │
│  │  │  Next.js 14 │  │  API Routes │  │  Middleware │  │  Edge Func  │  │   │
│  │  │  App Router │  │  (tRPC/REST)│  │  Auth/Rate  │  │  Webhooks   │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                              │                                              │
│                              ▼                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                        PYTHON BRAIN LAYER                             │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │   │
│  │  │  FastAPI    │  │  AI Engine  │  │  Analytics  │  │  Scheduler  │  │   │
│  │  │  Server     │  │  (Claude)   │  │  Engine     │  │  (Celery)   │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                              │                                              │
│                              ▼                                              │
│  ┌──────────────────────────┐  ┌─────────────────────────────────────────┐  │
│  │       SUPABASE           │  │              NEON                       │  │
│  │  (Primary — Realtime)    │  │  (Analytics + Archive + AI Vector DB)   │  │
│  │  ┌────────────────────┐  │  │  ┌────────────────────────────────────┐ │  │
│  │  │  PostgreSQL        │  │  │  │  PostgreSQL (Serverless)           │ │  │
│  │  │  Realtime Subs     │  │  │  │  pgvector (AI embeddings)          │ │  │
│  │  │  Auth              │  │  │  │  Time-Series (booking analytics)   │ │  │
│  │  │  Storage           │  │  │  │  Read Replicas                     │ │  │
│  │  │  Edge Functions    │  │  │  │  Connection Pooler                 │ │  │
│  │  └────────────────────┘  │  │  └────────────────────────────────────┘ │  │
│  └──────────────────────────┘  └─────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                     CLAUDE EXTENSIONS LAYER                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │   │
│  │  │  MCP Server │  │  Auto-Diag  │  │  Parts Rec  │  │  Content    │  │   │
│  │  │  (Model     │  │  (Vehicle   │  │  (AI Parts  │  │  Generator  │  │   │
│  │  │  Context)   │  │  Troublesh  │  │  Matcher)   │  │  (SEO/Blog) │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘

| #  | Page                   | Route              | Purpose                                    |
| -- | ---------------------- | ------------------ | ------------------------------------------ |
| 1  | **Home**               | `/`                | Hero, services preview, testimonials, CTA  |
| 2  | **About Us**           | `/about`           | Garage story, mission, values              |
| 3  | **Our Team**           | `/team`            | Mechanic profiles with certs & specialties |
| 4  | **Services Overview**  | `/services`        | All service categories grid                |
| 5  | **Service Detail**     | `/services/[slug]` | Individual service deep-dive               |
| 6  | **Pricing**            | `/pricing`         | Transparent service pricing tiers          |
| 7  | **Fleet / Commercial** | `/fleet`           | B2B fleet maintenance programs             |
| 8  | **Testimonials**       | `/reviews`         | Customer reviews with photos               |
| 9  | **Gallery**            | `/gallery`         | Before/after repair photos                 |
| 10 | **FAQ**                | `/faq`             | Common questions, searchable               |
| 11 | **Blog Index**         | `/blog`            | SEO articles, tips, news                   |
| 12 | **Blog Post**          | `/blog/[slug]`     | Individual article with related posts      |
| 13 | **Careers**            | `/careers`         | Open positions, culture                    |
| 14 | **Contact**            | `/contact`         | Form, map, hours, emergency line           |
| 15 | **Emergency Towing**   | `/emergency`       | 24/7 roadside assistance page              |
|16| **hidden admin panel  |edits,receiving analysts and bookings
| #  | Page                | Route                 | Purpose                          |
| -- | ------------------- | --------------------- | -------------------------------- |
| 26 | **Book Service**    | `/book`               | Multi-step booking wizard        |
| 27 | **Booking Success** | `/book/success`       | Confirmation + calendar invite   |
| 28 | **My Bookings**     | `/account/bookings`   | History, reschedule, cancel      |
| 29 | **Service Status**  | `/status/[bookingId]` | Live repair progress tracker     |
| 30 | **Drop-off Guide**  | `/drop-off`           | What to bring, parking, check-in |
| #  | Page                  | Route        | Purpose                              |
| -- | --------------------- | ------------ | ------------------------------------ |
| 31 | **AI Assistant**      | `/assistant` | Claude-powered chat interface        |
| 32 | **Vehicle Diagnosis** | `/diagnose`  | Symptom checker + AI troubleshooting |
| 33 | **Knowledge Base**    | `/kb`        | AI-curated repair guides             |
python-server/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI entry point
│   ├── config.py                  # Settings & env vars
│   │
│   ├── api/                       # REST API endpoints
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── bookings.py        # Booking CRUD + availability logic
│   │   │   ├── inventory.py       # Stock sync with Shopify
│   │   │   ├── analytics.py       # Business intelligence endpoints
│   │   │   ├── ai.py              # Claude AI endpoints
│   │   │   ├── webhooks.py        # Shopify + payment webhooks
│   │   │   └── health.py          # Health checks
│   │
│   ├── core/                      # Business logic
│   │   ├── __init__.py
│   │   ├── booking_engine.py      # Availability algorithm
│   │   ├── pricing_engine.py      # Dynamic pricing logic
│   │   ├── notification_service.py # Email/SMS dispatch
│   │   └── report_generator.py    # PDF invoices, reports
│   │
│   ├── ai/                        # Claude AI modules
│   │   ├── __init__.py
│   │   ├── claude_client.py       # Anthropic API wrapper
│   │   ├── diagnosis.py           # Vehicle symptom analysis
│   │   ├── parts_recommender.py   # AI parts matching
│   │   ├── content_generator.py   # SEO blog + product descriptions
│   │   ├── chat_memory.py         # Conversation history (vector DB)
│   │   └── mcp_server.py          # Model Context Protocol server
│   │
│   ├── models/                    # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── booking.py
│   │   ├── vehicle.py
│   │   ├── customer.py
│   │   └── ai.py
│   │
│   ├── services/                  # External integrations
│   │   ├── __init__.py
│   │   ├── shopify_client.py      # Shopify Admin API
│   │   ├── supabase_client.py     # Supabase SDK
│   │   ├── neon_client.py         # Neon serverless driver
│   │   ├── stripe_client.py       # Payment processing
│   │   ├── twilio_client.py       # SMS notifications
│   │   └── resend_client.py       # Transactional email
│   │
│   ├── tasks/                     # Background jobs (Celery)
│   │   ├── __init__.py
│   │   ├── sync_inventory.py      # Hourly Shopify stock sync
│   │   ├── send_reminders.py      # Daily booking reminders
│   │   ├── generate_reports.py    # Weekly analytics reports
│   │   └── ai_embeddings.py       # Vector index updates
│   │
│   └── utils/
│       ├── __init__.py
│       ├── validators.py
│       └── helpers.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── alembic/                       # Database migrations
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── vercel.json                    # Vercel serverless function config| Module                   | Function                                                                         |
| ------------------------ | -------------------------------------------------------------------------------- |
| **Booking Engine**       | Complex availability logic, bay scheduling, buffer times, holiday overrides      |
| **AI Diagnosis**         | Claude analyzes symptoms → suggests probable causes → recommends services        |
| **Parts Recommender**    | Matches vehicle VIN/specs to compatible parts using embeddings + Shopify catalog |
| **Content Generator**    | Auto-writes blog posts, product descriptions, email campaigns via Claude         |
| **Analytics Engine**     | Aggregates booking trends, revenue, parts sales → dashboards                     |
| **Notification Service** | Smart reminders (24h before, 1h before) via SMS/email with AI personalization    |
| **MCP Server**           | Exposes garage data to Claude Desktop for admin AI assistance                    |
| Feature                | Usage                                                    |
| ---------------------- | -------------------------------------------------------- |
| **PostgreSQL**         | Users, bookings, vehicles, garage config                 |
| **Auth**               | Customer accounts, OAuth (Google), magic links           |
| **Realtime**           | Live booking status updates, inventory changes           |
| **Storage**            | Vehicle photos, repair documentation, invoice PDFs       |
| **Edge Functions**     | Lightweight hooks (webhook validation, image transforms) |
| **Row Level Security** | Per-tenant data isolation                                |
