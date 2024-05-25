import io
import os
import base64
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from dash import Dash, html, dcc, Output, Input


def leer_datos():
    archivos = os.listdir("db")
    lista_dataframes = []
    last_number1 = -1
    last_number2 = -1
    
    for archivo in archivos:
        print(archivo)
        dataframe = pd.read_json("db/"+archivo, lines=True)
        dataframe["reviewTime"] = pd.to_datetime(
            dataframe["reviewTime"], format="%m %d, %Y"
        )
        
        dataframe["product_id"] = (
            pd.factorize(dataframe["asin"])[0] + last_number1 + 1
        )  # Creamos ids unicos por cada asin
        
        dataframe["person_id"] = (
            pd.factorize(dataframe["reviewerID"])[0] + last_number2 + 1
        )
        
        lista_dataframes.append(dataframe)
        last_number1 = dataframe["product_id"].max()
        last_number2 = dataframe["person_id"].max()

    df_grande = pd.concat(lista_dataframes, ignore_index=True)
    lista_dataframes.append(df_grande)
    
    return lista_dataframes

def dashboard(lista_dataframes):

    color_scale = px.colors.sequential.Viridis

    archivos = os.listdir("db")
    archivos.append('Everything') # Para poder mostrar visualizaciones de todos los productos.

    # Step 1. Create the dash app
    app = Dash(__name__)  # Creamos el Layout
    
    # Step 2. Set up the layout
    app.title = "Visualización de las reviews"

    # Step 3. the HTML component is defined
    app.layout = html.Div(
        children=[
            
            html.H1(children="Visualización de las reviews"),
            
            dcc.Dropdown(
                id="dropdown",  ## dropdown menu
                options=[
                    {
                        "label": archivos[i].replace("_5.json", "").replace("_", " "),
                        "value": int(i),
                    }
                    for i in range(len(archivos))
                ],
                value=0,
            ),
            
            html.H2(children="Evolución de reviews por años"),
            dcc.Graph(id="rev-per-year"),
            
            html.H2(children="Popularidad de los artículos"),
            dcc.Graph(id="art-popularity"),
            
            html.H2(children="Histograma por nota"),
            dcc.Graph(id="note-histogram"),
            
            html.H2(children="Evolución de las reviews a lo largo del tiempo"),
            dcc.Graph(id="time-evolution"),
            
            html.H2(children="Histograma de reviews por usuario."),
            dcc.Graph(id="reviews-per-user"),
            
            html.H2(children="Nube de palabras"),
            dcc.Graph(id="word-cloud"),
            
            html.H2(children="Longitudes de las reseñas"),
            dcc.Graph(id="summary-len"),
        ],
        
        style={"width": "100%", "display": "inline-block"},
    )

    @app.callback(
        [
            Output(component_id="rev-per-year", component_property="figure"),
            Output(component_id="art-popularity", component_property="figure"),
            Output(component_id="note-histogram", component_property="figure"),
            Output(component_id="time-evolution", component_property="figure"),
            Output(component_id="reviews-per-user", component_property="figure"),
            Output(component_id="word-cloud", component_property="figure"),
            Output(component_id="summary-len", component_property="figure"),
        ],
        
        Input(component_id="dropdown", component_property="value"),
    )
    
    def update_graph(i):
        filtered_dataframe = lista_dataframes[i].copy()
        filtered_dataframe["year"] = lista_dataframes[i]["reviewTime"].dt.year
        filtered_dataframe = filtered_dataframe.groupby("year").size()
        
        index = filtered_dataframe.index
        
        values = filtered_dataframe.values.tolist()
        
        data = {"index": index, "values": values}
        data = pd.DataFrame(data)
        
        rev_per_year = px.bar(
            data,
            x="index",
            y="values",
            title=f'Conteo de reviews por año {archivos[i].replace("_5.json", "").replace("_", " ")}',
            labels={"index": "Year", "values": "Conteo de reviews"},
            color_discrete_sequence=color_scale,
        )

        filtered_dataframe = lista_dataframes[i].copy()
        filtered_dataframe = (
            filtered_dataframe.groupby("product_id").size().sort_values(ascending=False)
        )
        
        index = list(filtered_dataframe.index)
        index = [str(i) for i in index]
        
        values = filtered_dataframe.values.tolist()
        
        data = {"index": index, "values": values}
        data = pd.DataFrame(data)
        
        rev_per_prod = px.line(
            data,
            x="index",
            y="values",
            title=f'Conteo de reviews por producto {archivos[i].replace("_5.json", "").replace("_", " ")}',
            labels={"index": "id producto", "values": "Conteo de reviews"},
            color_discrete_sequence=color_scale,
        )

        filtered_dataframe = lista_dataframes[i].copy()
        filtered_dataframe = filtered_dataframe.groupby("overall").size().sort_index()
        
        index = list(filtered_dataframe.index)
        index = [str(i) for i in index]
        
        values = filtered_dataframe.values.tolist()
        
        data = {"index": index, "values": values}
        data = pd.DataFrame(data)
        
        rev_per_not = px.bar(
            data,
            x="index",
            y="values",
            title=f'Conteo de reviews por nota {archivos[i].replace("_5.json", "").replace("_", " ")}',
            labels={"index": "nota", "values": "Conteo de reviews"},
            color_discrete_sequence=color_scale,
        )

        filtered_dataframe = lista_dataframes[i].copy()
        filtered_dataframe = (
            filtered_dataframe.groupby("unixReviewTime").size().sort_index()
        )
        
        index = list(filtered_dataframe.index)
        index = [str(i) for i in index]
        
        values = filtered_dataframe.values.tolist()
        
        data = {"index": index, "values": values}
        data = pd.DataFrame(data)
        data["values"] = data["values"].cumsum()
        
        time_evolution = px.line(
            data,
            x="index",
            y="values",
            title=f'Conteo de reviews por tiempo {archivos[i].replace("_5.json", "").replace("_", " ")}',
            labels={"index": "timestamp", "values": "Conteo de reviews"},
            color_discrete_sequence=color_scale,
        )

        filtered_dataframe = lista_dataframes[-1].copy()
        filtered_dataframe = filtered_dataframe.groupby("person_id").size().sort_index()
        
        index = list(filtered_dataframe.index)
        index = [str(i) for i in index]
        
        values = filtered_dataframe.values.tolist()
        
        data = {"index": index, "values": values}
        
        filtered_dataframe = pd.DataFrame(data).groupby("values").size()
        
        index = list(filtered_dataframe.index)
        index = [str(i) for i in index]
        
        values = filtered_dataframe.values.tolist()
        
        data = {"index": index, "values": values}
        data = pd.DataFrame(data)
        
        number_reviews_per_number_users = px.bar(
            data,
            x="index",
            y="values",
            title=f"reviews por numero de usuarios de Everything",
            labels={"index": "numero de reviews", "values": "numero de usuarios"},
            color_discrete_sequence=color_scale,
        )

        text = " ".join(lista_dataframes[i]["summary"])

        # Generar la nube de palabras
        wordcloud = WordCloud(background_color="white").generate(text)

        # Convertir la nube de palabras a una imagen
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")

        # Convertir la figura de matplotlib a una cadena base64
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        wordcloud_base64 = base64.b64encode(buf.read()).decode("utf-8")
        
        # Crear el objeto de figura para el componente Graph
        figure = {
            "data": [],
            "layout": {
                "images": [
                    {
                        "xref": "x",
                        "yref": "y",
                        "x": 1,
                        "y": 6,
                        "sizex": 3,
                        "sizey": 9,
                        "sizing": "stretch",
                        "layer": "below",
                        "source": "data:image/png;base64,{}".format(wordcloud_base64),
                    }
                ],
                "title": {
                    "text": f'Nube de palabras de las reseñas de {archivos[i].replace("_5.json", "").replace("_", " ")}'
                },
                "xaxis": {"visible": False},
                "yaxis": {"visible": False},
            },
        }

        review_lengths = lista_dataframes[i]["summary"].str.split().apply(len)
        review_lengths_counts = review_lengths.value_counts().sort_index()
        review_lengths_fig = px.bar(
            x=review_lengths_counts.index,
            y=review_lengths_counts.values,
            labels={
                "x": "Cantidad de palabras en la reseña",
                "y": "Cantidad de reseñas",
            },
            title=f'Distribución de longitudes de reseñas {archivos[i].replace("_5.json", "").replace("_", " ")}',
            color_discrete_sequence=color_scale,
        )

        return [
            rev_per_year,
            rev_per_prod,
            rev_per_not,
            time_evolution,
            number_reviews_per_number_users,
            figure,
            review_lengths_fig,
        ]

    app.run_server(debug=True, jupyter_mode="external")


if __name__ == "__main__":
    lista_dataframes = leer_datos()
    dashboard(lista_dataframes)