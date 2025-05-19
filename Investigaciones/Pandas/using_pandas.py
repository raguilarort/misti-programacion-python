import pandas as pd
import matplotlib.pyplot as plt

def staticarray():
    df = pd.DataFrame(
        {
            "Name": [
                "Braund, Mr. Owen Harris",
                "Allen, Mr. William Henry",
                "Bonnell, Miss. Elizabeth",
            ],
            "Age": [22, 35, 58],
            "Sex": ["male", "male", "female"],
        }
    )
    print("Contenido del arreglo dt: ")
    print(df)

    print("Imprimiento Columna edad:")
    print(df["Age"])
    
    print("Cuál es la mayor edad:")
    print(df["Age"].max())

def data_from_file():
    titanic = pd.read_csv("data/titanic.csv")

    print("Imprmiento contenido del archivo csv: ")
    print(titanic)

    print("Imprimientdo solo 8 filas")
    print(titanic.head(8))

    print("Imprimiendo tipos de datos de las columnas")
    print(titanic.dtypes)

def plot_functionality():
    air_quality = pd.read_csv("data/air_quality_no2.csv", index_col=0, parse_dates=True)
    print(air_quality.head())
    
    #air_quality["station_paris"].plot()
    #plt.show()
    #air_quality["station_london"].plot()
    #plt.show()

    air_quality.plot()
    plt.show()

    air_quality.plot.scatter(x="station_london", y="station_paris", alpha=0.5)
    plt.show()

    axs = air_quality.plot.area(figsize=(12, 4), subplots=True)
    plt.show()

# Función main
def main():

    #staticarray()
    #data_from_file()
    plot_functionality()


# Se invoca funcion main()
if __name__ == '__main__':
    main()