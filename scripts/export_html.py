#!/usr/bin/env python3
"""Export the notebook's committed outputs into docs/ for GitHub Pages.

This script does not re-run the analysis. It reads the figures and the
services-per-capita table that are already saved inside
helsinki_services_analysis.ipynb, so the published page always shows exactly the
numbers the notebook produced. The only thing it rebuilds is the choropleth
geometry, which is trimmed to the postal areas that actually carry data — the
copy embedded in the notebook contains every postal area in Finland and is ~40 MB.

Usage:
    pip install folium
    python scripts/export_html.py
"""
from __future__ import annotations

import ast
import base64
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
NOTEBOOK = ROOT / "helsinki_services_analysis.ipynb"
GEOJSON = ROOT / "Source_Data" / "finland-postal-codes.geojson"
DOCS = ROOT / "docs"
ASSETS = ROOT / "assets"

# Figures in notebook order, with the caption used on the landing page.
FIGURES = [
    ("children_per_daycare", "Children per daycare centre"),
    ("playgrounds_per_1000_children", "Playgrounds per 1,000 children"),
    ("sports_facilities_per_1000", "Sports facilities per 1,000 residents"),
    ("grocery_stores_per_1000", "Grocery stores per 1,000 residents"),
    ("pharmacies_per_10000", "Pharmacies per 10,000 residents"),
    ("alko_per_10000", "Alko stores per 10,000 residents"),
    ("employment_sectors", "Employment sector distribution"),
]


def load_notebook() -> dict:
    return json.loads(NOTEBOOK.read_text(encoding="utf-8"))


def extract_figures(nb: dict) -> None:
    """Write every committed PNG output to assets/ under its figure name."""
    ASSETS.mkdir(exist_ok=True)
    names = [name for name, _ in FIGURES]
    i = 0
    for cell in nb["cells"]:
        for out in cell.get("outputs", []):
            png = out.get("data", {}).get("image/png")
            if png is None:
                continue
            if i < len(names):
                (ASSETS / f"{names[i]}.png").write_bytes(base64.b64decode("".join(png)))
            i += 1
    print(f"  {min(i, len(names))} figures -> assets/")


def services_per_capita(nb: dict) -> list[dict]:
    """Read the committed ZIP/SPP table out of the notebook's saved output."""
    for cell in nb["cells"]:
        if "services_zip_dict" in "".join(cell["source"]) and cell.get("outputs"):
            for out in cell["outputs"]:
                text = "".join(out.get("text", "")).strip()
                if text.startswith("[{"):
                    return ast.literal_eval(text)
    raise SystemExit("could not find the services_zip_dict output in the notebook")


def build_map(rows: list[dict]) -> None:
    """Rebuild the choropleth, trimmed to postal areas that carry data."""
    import folium
    import pandas as pd

    data = pd.DataFrame(rows).drop_duplicates(subset="ZIP")
    wanted = set(data["ZIP"])

    gj = json.loads(GEOJSON.read_text(encoding="utf-8"))
    gj["features"] = [
        f for f in gj["features"]
        if f["properties"].get("postinumeroalue") in wanted
    ]
    print(f"  geojson trimmed to {len(gj['features'])} of the postal areas in the file")

    # The notebook used CartoDB Positron, which now requires an API key; OpenStreetMap
    # needs none and keeps the published map working for anyone who opens it.
    m = folium.Map(location=[60.16952, 24.93545], tiles="OpenStreetMap", zoom_start=11)
    folium.Choropleth(
        geo_data=gj,
        data=data,
        columns=["ZIP", "SPP"],
        key_on="feature.properties.postinumeroalue",
        fill_color="RdYlGn",
        nan_fill_color="transparent",
        fill_opacity=0.7,
        line_opacity=0.2,
        name="Services per capita",
        legend_name="Services per capita",
    ).add_to(m)

    folium.GeoJson(
        gj,
        control=False,
        style_function=lambda x: {
            "fillColor": "#ffffff", "color": "#000000",
            "fillOpacity": 0.1, "weight": 0.1,
        },
        highlight_function=lambda x: {
            "fillColor": "#000000", "color": "#000000",
            "fillOpacity": 0.5, "weight": 0.1,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["postinumeroalue"],
            aliases=["ZIP:"],
            style=("background-color: white; color: #333333; "
                   "font-family: arial; font-size: 12px; padding: 5px;"),
        ),
    ).add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)

    DOCS.mkdir(exist_ok=True)
    out = DOCS / "services_map.html"
    m.save(str(out))
    print(f"  {out.relative_to(ROOT)} ({out.stat().st_size / 1e6:.1f} MB)")


def copy_figures() -> None:
    target = DOCS / "assets"
    target.mkdir(parents=True, exist_ok=True)
    for name, _ in FIGURES:
        src = ASSETS / f"{name}.png"
        if src.exists():
            (target / f"{name}.png").write_bytes(src.read_bytes())
    print(f"  figures copied -> docs/assets/")


if __name__ == "__main__":
    print("Exporting committed outputs to docs/ ...")
    nb = load_notebook()
    extract_figures(nb)
    build_map(services_per_capita(nb))
    copy_figures()
    print("Done. docs/index.html is checked in and links to these files.")
