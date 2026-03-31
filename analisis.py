import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

# Cargar los datos desde el archivo CSV
retail_df= pd.read_csv(r'C:\Users\pedro\OneDrive\Documentos\Customer_analysis_project\online_retail.csv', encoding='latin1')
# Análisis exploratorio de datos
print(f"Forma del DataFrame: {retail_df.shape}")
#conocer las columnas del DataFrame
print(f"Columnas del DataFrame: {list(retail_df.columns)}")
#conocer los tipos de datos de cada columna
print(f"Tipos de datos: {retail_df.dtypes}")
#conocer las estadísticas descriptivas de las columnas numéricas
print(f"Estadísticas descriptivas: {retail_df.describe()}")
#conocer la cantidad de valores únicos en cada columna
print(f"Valores únicos por columna: {retail_df.nunique()}")
#conocer la cantidad de valores faltantes en cada columna
print(f"Valores faltantes por columna: {retail_df.isnull().sum()}")
#conocer la cantidad de valores nulos en cada columna
print(f"Valores nulos por columna: {retail_df.isnull().sum()}")

#Limpieza de datos
#Eliminar filas con valores faltantes
print("Shape original:", retail_df.shape)
retail_df=retail_df.dropna(subset=['CustomerID'])
print("Después de eliminar CustomerID nulos:", retail_df.shape)
#Eliminar devoluciones
retail_df=retail_df[retail_df['Quantity'] > 0]
print("Después de eliminar devoluciones:", retail_df.shape)
#Eliminar precios negativos o cero
retail_df=retail_df[retail_df['UnitPrice'] > 0]
print("Después de eliminar precios negativos o cero:", retail_df.shape)
#Crear columna Revenue
retail_df['Revenue'] = retail_df['Quantity'] * retail_df['UnitPrice']

#RFM Analysis(Recency, Frequency, Monetary)

#Revisión preliminar
print(f"Info del DataFrame después de limpieza: {retail_df.info()}")
#Cambio el tipo de dato de InvoiceDate a datetime para facilitar el análisis de tiempo y la creación de la columna Recency
retail_df['InvoiceDate'] = pd.to_datetime(retail_df['InvoiceDate'])
#Verificar el cambio de tipo de dato
print(f"Tipos de datos después de conversión: {retail_df.dtypes}")

#Fecha de compra mas reciente
print(f"Fecha de compra más reciente: {retail_df['InvoiceDate'].max()}")
#Definir la fecha de referencia para calcular Recency  
reference_date = snapshot_date = retail_df["InvoiceDate"].max() + dt.timedelta(days=1)
print(snapshot_date)

#Modificar customerID a string para evitar problemas en el análisis
retail_df['CustomerID'] = retail_df['CustomerID'].astype(str)
print(f"Tipos de datos después de conversión de CustomerID: {retail_df.dtypes}")
#Verificar cuantos unicos CustomerID hay después de la conversión
print(f"Cantidad de CustomerID únicos: {retail_df['CustomerID'].nunique()}")
#Calcular Recency, Frequency y Monetary para cada cliente
rfm = retail_df.groupby("CustomerID").agg({
    "InvoiceDate": "max", #Recency se calculará a partir de la fecha de compra más reciente
    "InvoiceNo": "count", #Frequency se calculará como el conteo de facturas por cliente
    "Revenue": "sum" #Monetary se calculará como la suma de los ingresos por cliente
})
#Renombrar las columnas para mayor claridad
rfm.columns = ["LastPurchaseDate", "Frequency", "Monetary"]
#Calcumaos Recency
rfm["Recency"] = (snapshot_date - rfm["LastPurchaseDate"]).dt.days
#Revisamos el resultado
print("Primeras filas del DataFrame RFM")
print(rfm.head())

#Revisamos las estadísticas descriptivas del DataFrame RFM
print("Estadísticas descriptivas del DataFrame RFM")
print(rfm.describe())
#Top clientes por gasto total (Monetary)
top_customers = rfm.sort_values("Monetary", ascending=False).head(10)
print("Top 10 clientes por gasto total (Monetary):")
print(top_customers)
#Top clientes por frecuencia de compra (Frequency)
top_frequent_customers = rfm.sort_values("Frequency", ascending=False).head(10)
print("Top 10 clientes por frecuencia de compra (Frequency):")
print(top_frequent_customers)
#clientes más recientes (Recency)
top_recent_customers = rfm.sort_values("Recency").head(10)
print("Top 10 clientes más recientes (Recency):")
print(top_recent_customers)
#clientes menos recientes (Recency)
top_least_recent_customers = rfm.sort_values("Recency", ascending=False).head(10)
print("Top 10 clientes menos recientes (Recency):")
print(top_least_recent_customers)
#Visualización de la identificacion de outliers en Monetary
plt.figure(figsize=(10, 6))
plt.hist(rfm["Monetary"], bins=50)
plt.title("Distribución de gasto (Monetary)")
plt.show()
#Visualización de clientes sin outliers
plt.hist(rfm["Monetary"], bins=100)
plt.xlim(0, 5000)
plt.title("Distribución de gasto (sin outliers extremos)")
plt.show()

#Segmentación de clientes utilizando RFM
#Asignar puntajes de RFM utilizando cuartiles
rfm["R_score"] = pd.qcut(rfm["Recency"], 4, labels=[4,3,2,1]) # Recency (menor = mejor → invertido)
rfm["F_score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 4, labels=[1,2,3,4]) # Frequency (mayor = mejor)
rfm["M_score"] = pd.qcut(rfm["Monetary"], 4, labels=[1,2,3,4]) # Monetary (mayor = mejor)
#Convertir a entero
rfm["R_score"] = rfm["R_score"].astype(int)
rfm["F_score"] = rfm["F_score"].astype(int)
rfm["M_score"] = rfm["M_score"].astype(int)
#Crear score combinado
rfm["RFM_Score"] = rfm["R_score"] + rfm["F_score"] + rfm["M_score"]
#Crear segmentos basados en los puntajes de RFM
def segment_customer(row):
    if row["R_score"] == 4 and row["F_score"] == 4:
        return "Champions"
    elif row["F_score"] >= 3:
        return "Loyal"
    elif row["R_score"] == 1:
        return "At Risk"
    else:
        return "Others"

rfm["Segment"] = rfm.apply(segment_customer, axis=1)
#Revisar la distribución de segmentos
print("Distribución de segmentos:")
print(rfm["Segment"].value_counts())
rfm.head()
#Tabla RFM con segmentos
print("Tabla RFM con segmentos:")
print(rfm[["Recency", "Frequency", "Monetary", "R_score", "F_score", "M_score", "RFM_Score", "Segment"]].head(10))

#Tabla resumen por segmento
segment_summary = rfm.groupby("Segment").agg(
    Revenue=("Monetary", "sum"),
    Avg_Frequency=("Frequency", "mean"),
    Avg_Recency=("Recency", "mean"),
    Num_Customers=("Monetary", "count")
)

segment_summary.sort_values(by="Revenue", ascending=False)
print("Resumen por segmento:")
print(segment_summary)

print("INSIGHTS DE NEGOCIO:\n")

print(f"1. El segmento que genera más dinero es: {segment_summary['Revenue'].idxmax()}")

print(f"2. El segmento con más clientes es: {segment_summary['Num_Customers'].idxmax()}")

print(f"3. El segmento que compra más seguido es: {segment_summary['Avg_Frequency'].idxmax()}")

print(f"4. El segmento con mayor recency (riesgo) es: {segment_summary['Avg_Recency'].idxmax()}")

#Crear tabla con recomendaciones de marketing para cada segmento
recommendations = pd.DataFrame({
    "Segment": ["Champions", "Loyal", "At Risk", "Others"],
    "Strategy": [
        "Retener clientes VIP, ofrecer recompensas y beneficios exclusivos",
        "Ofrecer promociones y cross-selling para aumentar el gasto",
        "Campañas de reactivación, descuentos y recordatorios",
        "Marketing general y promociones para aumentar frecuencia"
    ]
})

print(recommendations)
#Insight escrito
print("RECOMENDACIONES DE NEGOCIO:\n")

print("Champions: Son los mejores clientes, se deben retener y premiar.")
print("Loyal: Son clientes frecuentes, se puede aumentar su gasto.")
print("At Risk: Son clientes que no han comprado recientemente, se deben reactivar.")
print("Others: Son clientes promedio, se pueden trabajar con marketing general.")

#Visualizaciones
#Clientes por segmento
rfm["Segment"].value_counts().plot(kind="bar")
plt.title("Número de clientes por segmento")
plt.xlabel("Segmento")
plt.ylabel("Número de clientes")
plt.show()
#Revenue por segmento
rfm.groupby("Segment")["Monetary"].sum().plot(kind="bar")
plt.title("Revenue por segmento")
plt.xlabel("Segmento")
plt.ylabel("Revenue")
plt.show()
#Frecuencia por segmento
rfm.groupby("Segment")["Frequency"].mean().plot(kind="bar")
plt.title("Frecuencia promedio por segmento")
plt.xlabel("Segmento")
plt.ylabel("Frecuencia")
plt.show()
#Recency por segmento
rfm.groupby("Segment")["Recency"].mean().plot(kind="bar")
plt.title("Recency promedio por segmento")
plt.xlabel("Segmento")
plt.ylabel("Recency")
plt.show()

#Exportar resultados a CSV
rfm.to_csv(r'C:\Users\pedro\OneDrive\Documentos\Customer_analysis_project\rfm_analysis_results.csv')
segment_summary.to_csv(r'C:\Users\pedro\OneDrive\Documentos\Customer_analysis_project\segment_summary.csv')
recommendations.to_csv(r'C:\Users\pedro\OneDrive\Documentos\Customer_analysis_project\segment_recommendations.csv')
