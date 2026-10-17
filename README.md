# Logistics Network Planning Platform

**Collaborative Project · Application Engineering Portfolio**

A logistics planning platform that connects Excel-based workflows with a map interface. The original system helped planners explore warehouse locations and organize pickup or delivery routes using demand, transport costs and vehicle constraints.

## My Contribution
I contributed to selected software-engineering development tasks within a team. **I did not design or implement the warehouse-location or route-planning algorithms; those were contributions of other project members.**

This repository focuses on the application layer: interface logic, API interaction, workbook validation, workflow coordination and map presentation. It does not claim that I independently developed the entire platform or authored every retained line.

## Project Features
- Warehouse-planning forms with demand inputs and optional specified warehouses.
- Route-planning settings for pickup/delivery, routing strategy and calculation limits.
- Excel uploads, field validation and result-download handling.
- AMap interaction for location markers, route display and movement animation.

These describe capabilities of the original collaborative system. **The public repository excludes the team's algorithm implementations**, so it cannot calculate complete planning results on its own.

## Tech Stack and Architecture
The original platform used Vue 2, Element UI, Axios, Flask, pandas, Scikit-learn, OR-Tools and map APIs. The public application layer uses Vue 2, Vue Router, Element UI, Axios, Flask, pandas and AMap. Scikit-learn and OR-Tools belonged to the excluded algorithm layer.

```text
Excel input → Vue interface → Flask endpoints → team planning algorithms
                    ↑                                  ↓
             map presentation ← planning results / Excel export
```

```text
frontend/
  src/main.js, App.vue, router/    Application entry and navigation
  src/page/                       Warehouse and route screen logic
  src/api.js                      API request integration
  package.json, .env.example      Dependency and configuration references
backend/
  main.py                         Flask upload, planning and download endpoints
  service/                        Workflow coordination and route API boundary
  algorithm_boundary.py           Explicit boundary for omitted warehouse models
  utils/check.py                  Workbook schema and field validation
  paths.py, requirements.txt      Local paths and dependency reference
```

## Public Scope and Limitations
Business data, original Excel templates, private lookup tables, screenshots, third-party pictures/GeoJSON, collaborator utilities, old installers and compiled bundles are excluded. Map markers use SDK defaults; no map imagery or SDK implementation is bundled.

The warehouse model boundary raises `NotImplementedError`, which the workflow reports as a failure; the route boundary returns an explicit `unavailable` response. Neither provides a replacement algorithm. Address-helper integrations are also omitted. Existing result-download handlers require locally generated files that are not included.

The frontend entry and routes are retained, but the legacy bundler configuration is omitted. A compatible Vue 2 build setup must supply `AMAP_JS_KEY` and `AMAP_SECURITY_JS_CODE`; `.env.example` is a reference, not an automatically loaded configuration. Dependency manifests describe the historical stack, not a verified clean installation. This is source for portfolio review, not a production deployment package.

Python syntax, local module references, Vue script parsing and Vue template compilation were checked. Full installation, application builds, map calls and end-to-end planning were not verified. No measured performance or business savings are claimed.
