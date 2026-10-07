# Developement of Mangrove Forests on Hainan Island
# Geoscripting GRS 33806
# Group Project by Roxane Marguerat, Elmo van den Beld, Aleksandra Ananieva, Lea Ehrensperger
# Group proect challenge n.9

# Source: https://planetarycomputer.microsoft.com/docs/quickstarts/reading-stac
import os
import pystac_client
import planetary_computer
import odc.stac
import rioxarray

def search_landsat_scenes(years, bbox, max_cloud=40):
    """Search the STAC catalog and return valid scenes per year."""
    catalog = pystac_client.Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1",
        modifier=planetary_computer.sign_inplace,
    )

    selected_items = {}
    for year in years:
        time_range = f"{year}-01-01/{year}-01-31"
        platform = "landsat-5" if year < 2013 else "landsat-8"

        search = catalog.search(
            collections=["landsat-c2-l2"],
            bbox=bbox,
            datetime=time_range,
            query={
                "platform": {"eq": platform},
                "eo:cloud_cover": {"lt": max_cloud}
            },
        )
        items = search.get_all_items()
        print(f"Year {year}: Found {len(items)} scenes with <{max_cloud}% cloud cover.")
        selected_items[year] = list(items)

    return selected_items


def load_raw_landsat(selected_items, bbox, bands, output_dir="data/landsat_data"):
    """Load raw (unscaled) Landsat band data and save each band/year as a GeoTIFF."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    raw_data = {}
    for year, items in selected_items.items():
        if not items:
            print(f"No items found for year {year}")
            continue

        data = odc.stac.stac_load(
            items,
            bands=bands,
            bbox=bbox,
            crs="EPSG:32649",  # UTM Zone 49N for Hainan Island
            resolution=100,
            groupby="solar_day",
        )

        raw_data[year] = data

        # Save each band as its own GeoTIFF (one file per date, per band)
        for band in bands:
            for i, t in enumerate(data.time.values):
                out_path = os.path.join(output_dir, f"{band}_{year}_{i}.tif")
                data[band].isel(time=i).rio.to_raster(out_path)
                print(f"Saved {out_path}")

    return raw_data


# Execution
years = [1990]
bbox = [108.506470, 18.151072, 111.088257, 20.190035]
bands = ["red", "green", "blue", "nir08"]

selected_items = search_landsat_scenes(years, bbox, max_cloud=50)
raw_data = load_raw_landsat(selected_items, bbox, bands)