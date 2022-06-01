from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from cartopy import crs, feature

# READ & LOAD 
# -----------------------------------------------

def read_files_by_pattern(pattern, directory="./", ):
    return [str(file) for file in Path(directory).glob(pattern)]


def load_teseo_grid(grid_path):
    return pd.read_csv(grid_path, sep=" ", header=0, names=["lon", "lat", "depth"])


def load_teseo_particles_txt(pattern, directory):
    
    particle_files = read_files_by_pattern(pattern, directory)
    
    df=pd.DataFrame([])
    for file in particle_files:
        df = pd.concat(
            [
                df,
                pd.read_table(
                    file,
                    sep=",",
                    header=0,
                    encoding="iso-8859-1",
                    skipinitialspace=True,
                    names=[
                        "time",
                        "spill_id",
                        "subspill_id",
                        "lon",
                        "lat",
                        "depth",
                        "status_index",
                    ],
                ),
            ]
        )
    
    return df.sort_values("time")


def get_teseo_grid_extent(grid_path):
    df = load_teseo_grid(grid_path)
    return [df.lon.min(), df.lon.max(), df.lat.min(), df.lat.max()]


# PLOTTING 
# -----------------------------------------------

def plot_teseo_particles(t, dx, gshhs=None, extent=None):
    
    df_tmp = df.loc[df.time == t]

    if dx is not None:
        extent = [df_tmp.lon.min()-dx, df_tmp.lon.max()+dx, df_tmp.lat.min()-dx, df_tmp.lat.max()+dx]

    fig = plt.figure(figsize=[10, 10])
    ax = fig.add_subplot(1, 1, 1, projection=crs.PlateCarree())

    if extent is not None:
        ax.set_extent(extent, crs=crs.PlateCarree())
    if gshhs:
        ax.add_feature(feature.GSHHSFeature(scale="full")) 
    
    ax.add_feature(feature.LAND)
    ax.add_feature(feature.OCEAN)
    ax.add_feature(feature.COASTLINE)
    ax.add_feature(feature.BORDERS, linestyle=":")
    ax.add_feature(feature.LAKES, alpha=0.5)
    ax.add_feature(feature.RIVERS)
    ax.plot(df_tmp.lon, df_tmp.lat, marker="o", color="b")
    plt.show()


# MAIN 
# -----------------------------------------------

def main(directory, pattern, grid_path):

    extent = get_teseo_grid_extent(grid_path)
    df = load_teseo_particles_txt(pattern, directory)

    for t in df.time.unique():
        df_tmp = df.loc[df.time == t]
        plot_teseo_particles(df_tmp, dx=1)


if __name__ == "__main__":
    
    directory = '/home/aragong/repositories/plotting-notebooks/mock/TESEO_TOOLS_459612f0'
    pattern = '*particles*.txt'
    grid = '/home/aragong/repositories/plotting-notebooks/mock/TESEO_TOOLS_459612f0/input/grid.dat'
    
    main(directory, pattern, grid)




