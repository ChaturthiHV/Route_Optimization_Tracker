# ♻️ WasteTrack — Whitefield Waste Management System

A browser-based, real-time waste collection route optimization dashboard for the Whitefield area of Bengaluru, Karnataka. Built entirely with vanilla HTML, CSS, and JavaScript using Leaflet.js for map rendering.

---

## 📁 File Structure

```
├── index.html                          # Main login & depot dashboard entry point
├── login2.html                         # Alternate login page (Material-style)
├── user_dashboard.html                 # Live vehicle tracking view for residents
├── cutter.html                         # Dead-Mileage Cutter — route cost analysis
├── wf.html                           # Green Zone Skip Route Optimizer
├── density.html                        # Density-wise Collection — zone heatmap
├── market.html                         # Market Day Surge Mapper
├── whitefield_route_optimizer_demo.html # TSP route optimizer canvas demo
├── market_data.js                      # GeoJSON data for market surge zones
└── data/
    ├── whitefield.geojson
    ├── whitefield_line.geojson ... (line1–5)
    ├── loc1.geojson
    ├── depot.geojson
    └── deport_point.geojson
```

---

## 🚀 Features

### 🔐 Login (`index.html` / `login2.html`)
- Dual-role login: **User** (vehicle tracking) and **Depot** (dashboard)
- Animated map-like background with road grid and green zone overlays
- Live status indicator

### 🗺️ Depot Dashboard (`index.html` → Depot login)
- Interactive Leaflet map centered on Whitefield
- Toggleable layers: road network, NDVI/green zones, collection nodes
- Quick-launch buttons to all sub-modules

### 🚛 User Dashboard (`user_dashboard.html`)
- Real-time animated truck tracking for 3 waste collection routes:
  - **Route A** — Whitefield Main
  - **Route B** — Marathahalli
  - **Route C** — ITPL Zone
- Road-following animation via OSRM routing API (falls back to straight-line)
- Vehicle status, progress bars, stop-by-stop breakdown
- Satellite / Road / Dark map modes

### ✂️ Dead-Mileage Cutter (`cutter.html`)
- Visualizes straight-line routes from a central dump yard (Whitefield) to 38 collection zones
- Color-coded by distance (near/mid/far)
- Per-zone cost breakdown: distance (km), fuel (L), cost (₹)
- Interactive zone list with detail panel
- Toggleable layers: routes, zone grid, dump yard

### 🌿 Green Zone Skip Route Optimizer(`wf.html`)
- Detects low or no waste areas and represents them as a **green coloured layer (parks or green areas)**, while waste-generating zones are shown as a **yellow coloured layer (buildings, residential, commercial areas)**  
- Removes green zones from the planned route to avoid unnecessary stops and redundant coverage 
- Focuses collection only on yellow layer zones, ensuring routes cover only active waste-generating areas 

### 📊 Density-wise Collection (`density.html`)
- Raster overlay showing waste generation density across the grid
- Three density tiers:
  - 🟢 **Low** — 1 collection/week
  - 🟠 **Medium** — 3 collections/week
  - 🔴 **High** — daily collection
- Zone filtering by density card
- Per-zone detail: vehicles, distance, fuel, cost

### 🛒 Market Day Surge Mapper (`market.html`)
- Detects current day (Thursday / Sunday = market surge days)
- Displays surge zones sourced from OSM / QGIS data
- 9 extra Whitefield market locations with distinct icons by surge type (Thu-only, Sun-only, Both)
- QuickOSM overlay, layer toggles, animated surge route activation
- Right panel: waste stats, zone schedule, collection route list

### 🧮 Route Optimizer Demo (`whitefield_route_optimizer_demo.html`)
- Canvas-based Nearest-Neighbour TSP vs. naive sequential comparison
- Configurable number of collection points and day filter
- Animated route drawing with distance labels and stop order numbers

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Maps | [Leaflet.js](https://leafletjs.com/) v1.9.3 |
| Tile Providers | OpenStreetMap, Esri World Imagery, CartoDB Dark |
| Routing | [OSRM](https://project-osrm.org/) (public API) |
| Clustering | Leaflet.markercluster v1.5.3 |
| Data format | GeoJSON (inline + external files) |
| Fonts | Space Grotesk, JetBrains Mono, Barlow (Google Fonts) |
| Language | Vanilla HTML5 / CSS3 / ES6 JavaScript |


---

## 📍 Geographic Coverage

All data covers the **Whitefield** area of Bengaluru, Karnataka, India.

- Dump yard hub: `13.0111°N, 77.7713°E` (Whitefield)
- Grid: 38 collection zones across a ~5 km × 4 km area
- Coordinates range: `12.976°N–13.016°N`, `77.731°E–77.779°E`

---

