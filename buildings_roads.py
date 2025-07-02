import osmnx as ox
import geopandas as gpd

place = "Baikalsk, Irkutsk Oblast, Russia"

# 1. Скачиваем все здания
print("Скачивание зданий...")
buildings = ox.features_from_place(place, tags={"building": True})

res_types = ["residential", "apartments", "house", "detached", "terrace", "semidetached_house", "yes"]
gdf = buildings[buildings["building"].isin(res_types)].copy()

color_map = {
    "apartments": "#6a3d9a",
    "residential": "#1f78b4",
    "house": "#b15928",
    "detached": "#33a02c",
    "terrace": "#ff7f00",
    "semidetached_house": "#cab2d6",
    "yes": "#b2b2b2",
}
gdf["color"] = gdf["building"].map(color_map).fillna("#000000")

levels_col = gdf.get("building:levels")
if "levels" in gdf.columns:
    levels_col = levels_col.combine_first(gdf["levels"])

gdf["num_levels"] = levels_col.fillna("1").astype(str)

print("Сохранение зданий...")
gdf[["geometry", "building", "num_levels", "color"]].to_file(
    "baikalsk_residential_all_colored.geojson", driver="GeoJSON"
)

# 2. ДОРОГИ
print("Получение координат центра Байкальска...")
city = ox.geocode_to_gdf(place)
center = city.geometry.centroid.iloc[0]

print("Скачивание дорог в радиусе 40 км...")
graph = ox.graph_from_point((center.y, center.x), dist=40000, network_type="all", simplify=True)

edges = ox.graph_to_gdfs(graph, nodes=False, edges=True)
edges_gdf = edges[["geometry", "highway"]]

edges_gdf.to_file("baikal_roads.geojson", driver="GeoJSON")
edges_gdf.to_file("baikal_roads.shp", driver="ESRI Shapefile")

