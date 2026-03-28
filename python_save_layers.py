"""
python_save_layers.py
=====================
Run this from the QGIS Python Console (Plugins > Python Console > Run Script)
or from a QGIS Processing script.

Saves every loaded layer to:
  - GeoJSON  (.geojson)
  - Shapefile (.shp)

Output folder: <project_dir>/export_layers/

Layers covered:
  - whitefield_boundary
  - whitefield_roads
  - market_3
  - market_surge_zones
  - (any other vector layers present in the project)
"""

import os
import json
from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsVectorFileWriter,
    QgsCoordinateTransformContext,
    QgsCoordinateReferenceSystem,
)
from qgis.utils import iface

# ── CONFIG ───────────────────────────────────────────────────────────────────

# Target CRS: WGS84 (EPSG:4326) for GeoJSON / web use
TARGET_CRS = QgsCoordinateReferenceSystem("EPSG:4326")

# Output directory — placed next to the .qgz project file
project_path = QgsProject.instance().homePath()
if not project_path:
    # Fallback if project not saved yet
    import tempfile
    project_path = tempfile.gettempdir()

OUTPUT_DIR = os.path.join(project_path, "export_layers")
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"📁  Exporting layers to: {OUTPUT_DIR}")
print("=" * 60)

# ── HELPERS ──────────────────────────────────────────────────────────────────

def sanitize(name: str) -> str:
    """Replace unsafe chars for filenames."""
    return "".join(c if c.isalnum() or c in "_-" else "_" for c in name)


def save_layer(layer: QgsVectorLayer, out_dir: str):
    """Save a single vector layer to GeoJSON and Shapefile."""
    if not layer.isValid():
        print(f"  ⚠️  Skipping invalid layer: {layer.name()}")
        return

    safe_name = sanitize(layer.name())
    results = {}

    # ── GeoJSON ──────────────────────────────────────────────────────────────
    geojson_path = os.path.join(out_dir, f"{safe_name}.geojson")
    options_geojson = QgsVectorFileWriter.SaveVectorOptions()
    options_geojson.driverName = "GeoJSON"
    options_geojson.fileEncoding = "UTF-8"
    options_geojson.ct = QgsCoordinateTransformContext()
    options_geojson.destCRS = TARGET_CRS

    error_geojson, msg_geojson, _, _ = QgsVectorFileWriter.writeAsVectorFormatV3(
        layer, geojson_path, QgsCoordinateTransformContext(), options_geojson
    )

    if error_geojson == QgsVectorFileWriter.NoError:
        results["geojson"] = "✅"
    else:
        results["geojson"] = f"❌ {msg_geojson}"

    # ── Shapefile ─────────────────────────────────────────────────────────────
    shp_path = os.path.join(out_dir, f"{safe_name}.shp")
    options_shp = QgsVectorFileWriter.SaveVectorOptions()
    options_shp.driverName = "ESRI Shapefile"
    options_shp.fileEncoding = "UTF-8"
    options_shp.ct = QgsCoordinateTransformContext()
    options_shp.destCRS = TARGET_CRS

    error_shp, msg_shp, _, _ = QgsVectorFileWriter.writeAsVectorFormatV3(
        layer, shp_path, QgsCoordinateTransformContext(), options_shp
    )

    if error_shp == QgsVectorFileWriter.NoError:
        results["shp"] = "✅"
    else:
        results["shp"] = f"❌ {msg_shp}"

    feat_count = layer.featureCount()
    print(f"  {results['geojson']} GeoJSON  | {results['shp']} SHP  →  {safe_name}  ({feat_count} features)")


# ── ALSO WRITE market_data.js EQUIVALENT ────────────────────────────────────

def layer_to_geojson_dict(layer: QgsVectorLayer) -> dict:
    """Convert a QgsVectorLayer to a plain GeoJSON dict."""
    features = []
    for feat in layer.getFeatures():
        geom = feat.geometry()
        if geom is None:
            continue
        geom.transform(
            # no transform needed if already EPSG:4326
            # add QgsCoordinateTransform if needed
        )
        properties = {field.name(): feat[field.name()] for field in layer.fields()}
        try:
            geo_json_str = geom.asJson(precision=8)
            geo_dict = json.loads(geo_json_str)
        except Exception:
            geo_dict = {}

        features.append({
            "type": "Feature",
            "properties": properties,
            "geometry": geo_dict
        })

    return {
        "type": "FeatureCollection",
        "name": layer.name(),
        "features": features
    }


def save_market_data_js(layers_dict: dict, out_dir: str):
    """
    Writes a market_data.js file combining all layers as JS variables,
    exactly matching the format used by market.html.
    """
    js_path = os.path.join(out_dir, "market_data.js")
    var_map = {
        "market_surge_zones": "SURGE_GEO",
        "whitefield_boundary": "BOUNDARY_GEO",
        "whitefield_roads": "ROADS_GEO",
        "market_3": "MARKET3_GEO",
    }

    lines = []
    for layer_name, var_name in var_map.items():
        if layer_name in layers_dict:
            geo_dict = layer_to_geojson_dict(layers_dict[layer_name])
            lines.append(f"var {var_name} = {json.dumps(geo_dict, indent=2)};\n")
        else:
            lines.append(f"// Layer '{layer_name}' not found in project\nvar {var_name} = {{\"type\":\"FeatureCollection\",\"features\":[]}};\n")

    with open(js_path, "w", encoding="utf-8") as fh:
        fh.write("// Auto-generated by python_save_layers.py (QGIS export)\n")
        fh.write("// Do not edit manually.\n\n")
        fh.writelines(lines)

    print(f"\n✅  market_data.js written → {js_path}")


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    root = QgsProject.instance().layerTreeRoot()
    all_layers = QgsProject.instance().mapLayers().values()

    # Only vector layers
    vector_layers = [l for l in all_layers if isinstance(l, QgsVectorLayer)]

    print(f"Found {len(vector_layers)} vector layer(s).\n")

    layers_by_name = {}
    for layer in vector_layers:
        print(f"Saving: {layer.name()}")
        save_layer(layer, OUTPUT_DIR)
        layers_by_name[layer.name().lower()] = layer

    # Write combined market_data.js
    save_market_data_js(layers_by_name, OUTPUT_DIR)

    # Summary JSON of what was exported
    summary = {
        "exported_layers": [l.name() for l in vector_layers],
        "output_dir": OUTPUT_DIR,
        "crs": TARGET_CRS.authid(),
        "formats": ["GeoJSON", "Shapefile"],
        "market_data_js": "market_data.js",
    }
    summary_path = os.path.join(OUTPUT_DIR, "export_summary.json")
    with open(summary_path, "w") as fh:
        json.dump(summary, fh, indent=2)

    print("\n" + "=" * 60)
    print(f"✅  Export complete!  {len(vector_layers)} layers → {OUTPUT_DIR}")
    print(f"📄  Summary: {summary_path}")
    print("=" * 60)


main()