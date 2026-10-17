# Logistics Network Planning Platform

**Collaborative project | Software engineering portfolio**

A logistics planning application designed to bring warehouse-location and transportation-route planning workflows into a single interface. The original team project combined structured Excel inputs, planning algorithms, backend services, and interactive map visualizations to help users explore logistics planning scenarios.

## Key Features

- **Warehouse planning:** Enter demand information and configure candidate or specified warehouse locations.
- **Route planning:** Set up pickup and delivery scenarios, routing strategies, and calculation constraints.
- **Excel workflows:** Upload planning inputs, validate fields, and handle generated result files.
- **Map visualization:** Display locations and routes through AMap, including marker and movement visualization features.

These features describe the original collaborative system. The public repository contains a selected portion of its application code, not the complete working platform.

## Technology Stack

| Layer | Technologies |
| --- | --- |
| Frontend | Vue 2, Vue Router, Element UI, Axios |
| Backend | Python, Flask, pandas |
| Mapping | AMap (Gaode Maps) APIs |
| Original team's algorithm layer (not included) | Scikit-learn, OR-Tools |

## My Contribution

I contributed to **selected software engineering and application development tasks** as part of the project team. My work was on the engineering side rather than the design or implementation of the core warehouse-location and route-planning algorithms, which were developed by other team members.

This portfolio repository highlights the platform's application-layer structure and illustrates how its user interface, backend endpoints, data-validation workflows, and mapping integration fit together. It should not be taken to mean that I individually authored every included component.

## How the System Fits Together

```text
Excel planning inputs
         |
         v
Vue interface and forms
         |
         v
Flask API and workflow coordination
         |
         v
Team planning algorithms (not published)
         |
         v
Planning results -> Excel output / map visualization
```

The public source includes the following selected components:

```text
frontend/   Vue views, routing, API integration, and configuration examples
backend/    Flask endpoints, workflow services, validation, and integration boundaries
```

## About This Public Version

This is a **portfolio-oriented excerpt of an earlier collaborative project**, not a ready-to-deploy application. The team's planning algorithms, operational datasets, original Excel templates, certain third-party assets, and historical build artifacts are intentionally excluded. As a result, warehouse and route calculations cannot run end to end from this repository alone.

Some original build configuration and integrations are also absent. API credentials are not included; any future local setup would require appropriate map-service credentials and a compatible legacy environment. Basic source and template checks were performed, but a clean installation and full application run have not been verified.
