import plotly.express as px
import folium
import branca

df = px.data.gapminder().query("country=='Canada'")
fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')
fig.update_layout(margin=dict(t=30,l=10,b=10,r=10))
fig.write_html('data/kiemrtra.html')

filepath = 'data/kiemrtra.html'
with open(filepath , encoding='utf-8') as f:
    html = f.read()

coor1= [19.742110608748604, -99.01751491998121]
geomap = folium.Map([19.715576, -99.20099], zoom_start=9, tiles="OpenStreetMap")

iframe = branca.element.IFrame(html=html, width=500, height=300)
popup = folium.Popup(iframe, max_width=500)

folium.Marker([coor1[0],coor1[1]], popup=popup).add_to(geomap)

geomap