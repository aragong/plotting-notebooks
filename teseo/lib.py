from pathlib import Path
import ipywidgets as widgets
import matplotlib.pyplot as plt
import pandas as pd
from cartopy import crs, feature
import numpy as np


def get_time_panel(df):
    play = widgets.Play(
        value=df.time.unique().min(),
        min=df.time.unique().min(),
        max=df.time.unique().max(),
        step=np.unique(np.diff(df.time.unique())),
        interval=500,
        description="Press play",
        disabled=False,
    )

    time_slider = widgets.FloatSlider(
        value=df.time.unique().min(),
        min=df.time.unique().min(),
        max=df.time.unique().max(),
        step=np.unique(np.diff(df.time.unique())),
        description='Time (h):',
        readout_format='.1f',
    )
    widgets.jslink((play, 'value'), (time_slider, 'value'))


    return widgets.HBox([play, time_slider]), time_slider , play


def get_fixed_widgets():

    directory_box = widgets.Text(
        # value="/home/aragong/repositories/plotting-notebooks/mock/TESEO_TOOLS_459612f0",
        placeholder='Type something',
        description='Directory:',
        disabled=False
    )

    pattern_box = widgets.Select(
        options=['*_particles_*.txt', '*_properties_*.txt', '*_grid_*.txt'],
        description='File-pattern:',
        disabled=False
    )

    dx_slider = widgets.FloatSlider(
        value=1.000,
        min=0.000,
        max=10.000,
        step=0.02,
        description='Zoom out:',
        readout_format='.3f',
    )

    psize_slider =  widgets.IntSlider(
        value=1,
        min=1,
        max=50,
        step=1,
        description='Particle size:',
    )

    grid_checkbox = widgets.Checkbox(
        value=True,
        description='Gridlines',
        disabled=False,
        indent=False
    )

    gshhs_checkbox = widgets.Checkbox(
        value=True,
        description='GSHHS',
        disabled=False,
        indent=False
    )

    pmarker_box = widgets.Dropdown(
        options=[("point", "o"), ("cross", "x"), ("square", "s")],
        value="x",
        description='Marker',
    )

    pcolor_box = widgets.Dropdown(
        options=["blue", "red", "black", "green", "yellow", "brown"],
        value="blue",
        description='Color',
    )
    
    return directory_box, pattern_box, dx_slider, psize_slider, grid_checkbox, gshhs_checkbox, pmarker_box, pcolor_box



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

def plot_teseo_particles(df, t, dx, pmarker, pcolor, psize, grid,  gshhs=None, extent=None):
    
    fig = plt.figure(figsize=[15, 10])
    ax = fig.add_subplot(1, 1, 1, projection=crs.PlateCarree())
    
    df_tmp = df.loc[df.time == t]

    if dx is not None:
        extent = [df_tmp.lon.min()-dx, df_tmp.lon.max()+dx, df_tmp.lat.min()-dx, df_tmp.lat.max()+dx]

    if extent is not None:
        ax.set_extent(extent, crs=crs.PlateCarree())
    

    
    gl = ax.gridlines(crs=crs.PlateCarree(), draw_labels=True,
                  linewidth=0.5, color='black', alpha=0.8, linestyle='--')
    
    gl.top_labels = False
    gl.left_labels = False
    
    if grid is False:
        gl.xlines = False
        gl.ylines = False
    if gshhs:
        ax.add_feature(feature.GSHHSFeature(scale="full", facecolor="grey"))
    else:
        ax.add_feature(feature.LAND)
        ax.add_feature(feature.COASTLINE)
    ax.add_feature(feature.OCEAN)
    ax.add_feature(feature.BORDERS, linestyle=":")
    ax.add_feature(feature.LAKES, alpha=0.5)
    ax.add_feature(feature.RIVERS)
    ax.scatter(df_tmp.lon, df_tmp.lat, marker=pmarker, c=pcolor, s=psize)

    ax.set_adjustable('datalim')


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




