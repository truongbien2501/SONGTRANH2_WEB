import geopandas as gpd
import folium
import json

gdf = gpd.read_file(r'C:\Users\Admin\Desktop\HoAVuong\SongTranh2.shp')

gdf_wgs84 = gdf.to_crs(epsg=4326)

# with open('file_json.json', 'r') as f:
#     data = json.load(f)
# # print(gdf_wgs84)
# m = folium.Map(location=[15.3371600,108.39232], 
#                 zoom_start=6,
#                 width='95%',  # Định dạng kích thước chiều rộng
#                 height='100%',# Định dạng kích thước chiều cao
#                 crs= 'EPSG3857'
#             )
# folium.GeoJson(data=data, name='geometry').add_to(m)
# m.show_in_browser()
# # # # print(gdf)

j = gdf_wgs84.to_json()
# Lưu dữ liệu vào tệp với tên file_json.json
with open('SongTranh2.json', 'w') as f:
    json.dump(j, f)
# print(j)
# for _, r in gdf.iterrows():
#     #without simplifying the representation of each borough, the map might not be displayed
#     #sim_geo = gpd.GeoSeries(r['geometry'])
#     sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
#     geo_j = sim_geo.to_json()
#     geo_j = folium.GeoJson(data=geo_j,
#                            style_function=lambda x: {'fillColor': 'orange'})
#     # folium.Popup(r['BoroName']).add_to(geo_j)
#     geo_j.add_to(m)
# m.show_in_browser()