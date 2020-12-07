def main():
    import matplotlib.pyplot as plt
    import pyart
    import netCDF4
    from glob import glob
    import os
    import numpy as np
    import cartopy.crs as ccrs
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    def plot_imd_radar(fpath, ele, plotpath):
        # Plotting Options Set in Function
        # ele = 0 #Elevation
        # R = 50#  #Min and Mac Range from Radar in km

        # Read Files and Setup Plotting
        radar = pyart.io.read(fpath)
        display = pyart.graph.RadarMapDisplay(radar)

        # set the figure title and show
        instrument_name = (radar.metadata['instrument_name'])[0:7]
        time_start = netCDF4.num2date(radar.time['data'][0], radar.time['units'])
        time_text = ' ' + time_start.strftime('%Y-%m-%d %H:%M:%SZ')

        elevation = radar.fixed_angle['data'][ele]
        ele_text = '%0.1f' % (elevation)

        title = instrument_name + time_text + ' Elevation %.1f' % (elevation)

        if np.round(elevation, 0) > 9.99:
            ele_folder = 'ele' + ele_text[0] + ele_text[1] + '_' + ele_text[3] + '/'
            ele_name = 'ele' + ele_text[0] + ele_text[1] + '_' + ele_text[3]
        else:
            ele_folder = 'ele' + ele_text[0] + '_' + ele_text[2] + '/'
            ele_name = 'ele' + ele_text[0] + '_' + ele_text[2]

        plot_file_name = instrument_name + '_' + time_start.strftime('%Y-%m-%dT%H%M%SZ') + ele_name + '.png'

        loc_folder = instrument_name + '/'

        fig_save_file_path = plotpath + loc_folder + ele_folder

        if os.path.isfile(fig_save_file_path + plot_file_name):
            print(fig_save_file_path + plot_file_name + ' exists')
        else:
            # Figure Options
            width = 30  # in inches
            height = 10  # in inches

            fig = plt.figure(figsize=(width, height))
            nrows = 2
            ncols = 5

            # Setting projection and ploting the second tilt
            projection = ccrs.LambertConformal(central_latitude=radar.latitude['data'][0],
                                               central_longitude=radar.longitude['data'][0])
            x = 0.4

            ax1 = fig.add_subplot(nrows, ncols, 1, projection=projection)
            display.plot_ppi_map('dBZ', ele, ax=ax1, vmin=-32, vmax=16., title='Horizontal Reflectivity',
                                 colorbar_label=radar.fields['dBZ']['units'],
                                 min_lon=radar.longitude['data'][0] - 2 * x, max_lon=radar.longitude['data'][0] + 2 * x,
                                 min_lat=radar.latitude['data'][0] - 2 * x,
                                 max_lat=radar.latitude['data'][0] + 2 * x, lon_lines=np.arange(52, 58, .4),
                                 resolution='10m', lat_lines=np.arange(15.5, 18.5, .2),
                                 projection=projection, fig=fig, lat_0=radar.latitude['data'][0],
                                 lon_0=radar.longitude['data'][0])
            display.plot_range_ring(25., line_style='k--', lw=1)
            display.plot_range_ring(50., line_style='k-', lw=0.5)
            display.plot_range_ring(75., line_style='k--', lw=1)
            display.plot_range_ring(100., line_style='k-', lw=0.5)
            display.plot_range_ring(125., line_style='k--', lw=1)
            display.plot_range_ring(150., line_style='k-', lw=0.5)
            # Indicate the radar location with a point
            display.plot_point(radar.longitude['data'][0], radar.latitude['data'][0], 'ko')

            ax2 = fig.add_subplot(nrows, ncols, 2, projection=projection)
            display.plot_ppi_map('ZDR', ele, ax=ax2, vmin=-2, vmax=10., title='Differential Reflectivity',
                                 colorbar_label=radar.fields['ZDR']['units'], cmap='pyart_RefDiff',
                                 min_lon=radar.longitude['data'][0] - 2 * x, max_lon=radar.longitude['data'][0] + 2 * x,
                                 min_lat=radar.latitude['data'][0] - 2 * x, max_lat=radar.latitude['data'][0] + 2 * x,
                                 lon_lines=np.arange(52, 58, .4), resolution='10m',
                                 lat_lines=np.arange(15.5, 18.5, .2), projection=projection,
                                 fig=fig, lat_0=radar.latitude['data'][0],
                                 lon_0=radar.longitude['data'][0])
            display.plot_range_ring(25., line_style='k--', lw=1)
            display.plot_range_ring(50., line_style='k-', lw=0.5)
            display.plot_range_ring(75., line_style='k--', lw=1)
            display.plot_range_ring(100., line_style='k-', lw=0.5)
            display.plot_range_ring(125., line_style='k--', lw=1)
            display.plot_range_ring(150., line_style='k-', lw=0.5)
            # Indicate the radar location with a point
            display.plot_point(radar.longitude['data'][0], radar.latitude['data'][0], 'ko')

            ax3 = fig.add_subplot(nrows, ncols, 3, projection=projection)
            display.plot_ppi_map('RhoHV', ele, ax=ax3, vmin=.5, vmax=1., title='Cross Correlation Ratio',
                                 colorbar_label=radar.fields['RhoHV']['units'], cmap='pyart_RefDiff',
                                 min_lon=radar.longitude['data'][0] - 2 * x, max_lon=radar.longitude['data'][0] + 2 * x,
                                 min_lat=radar.latitude['data'][0] - 2 * x, max_lat=radar.latitude['data'][0] + 2 * x,
                                 lon_lines=np.arange(52, 58, .4), resolution='10m',
                                 lat_lines=np.arange(15.5, 18.5, .2), projection=projection,
                                 fig=fig, lat_0=radar.latitude['data'][0],
                                 lon_0=radar.longitude['data'][0])
            display.plot_range_ring(25., line_style='k--', lw=1)
            display.plot_range_ring(50., line_style='k-', lw=0.5)
            display.plot_range_ring(75., line_style='k--', lw=1)
            display.plot_range_ring(100., line_style='k-', lw=0.5)
            display.plot_range_ring(125., line_style='k--', lw=1)
            display.plot_range_ring(150., line_style='k-', lw=0.5)
            # Indicate the radar location with a point
            display.plot_point(radar.longitude['data'][0], radar.latitude['data'][0], 'ko')

            ax4 = fig.add_subplot(nrows, ncols, 4, projection=projection)
            display.plot_ppi_map('KDP', ele, ax=ax4, vmin=-2, vmax=5., title='Specific Differential Phase',
                                 colorbar_label=radar.fields['KDP']['units'], cmap='pyart_Theodore16',
                                 min_lon=radar.longitude['data'][0] - 2 * x, max_lon=radar.longitude['data'][0] + 2 * x,
                                 min_lat=radar.latitude['data'][0] - 2 * x, max_lat=radar.latitude['data'][0] + 2 * x,
                                 lon_lines=np.arange(52, 58, .4), resolution='10m',
                                 lat_lines=np.arange(15.5, 18.5, .2), projection=projection,
                                 fig=fig, lat_0=radar.latitude['data'][0],
                                 lon_0=radar.longitude['data'][0])
            display.plot_range_ring(25., line_style='k--', lw=1)
            display.plot_range_ring(50., line_style='k-', lw=0.5)
            display.plot_range_ring(75., line_style='k--', lw=1)
            display.plot_range_ring(100., line_style='k-', lw=0.5)
            display.plot_range_ring(125., line_style='k--', lw=1)
            display.plot_range_ring(150., line_style='k-', lw=0.5)
            # Indicate the radar location with a point
            display.plot_point(radar.longitude['data'][0], radar.latitude['data'][0], 'ko')

            ax5 = fig.add_subplot(nrows, ncols, 5, projection=projection)
            display.plot_ppi_map('PhiDP', ele, ax=ax5, vmin=-180, vmax=180., title='Differential Phase',
                                 colorbar_label=radar.fields['PhiDP']['units'], cmap='pyart_Wild25',
                                 min_lon=radar.longitude['data'][0] - 2 * x, max_lon=radar.longitude['data'][0] + 2 * x,
                                 min_lat=radar.latitude['data'][0] - 2 * x, max_lat=radar.latitude['data'][0] + 2 * x,
                                 lon_lines=np.arange(52, 58, .4), resolution='10m',
                                 lat_lines=np.arange(15.5, 18.5, .2), projection=projection,
                                 fig=fig, lat_0=radar.latitude['data'][0],
                                 lon_0=radar.longitude['data'][0])
            display.plot_range_ring(25., line_style='k--', lw=1)
            display.plot_range_ring(50., line_style='k-', lw=0.5)
            display.plot_range_ring(75., line_style='k--', lw=1)
            display.plot_range_ring(100., line_style='k-', lw=0.5)
            display.plot_range_ring(125., line_style='k--', lw=1)
            display.plot_range_ring(150., line_style='k-', lw=0.5)
            # Indicate the radar location with a point
            display.plot_point(radar.longitude['data'][0], radar.latitude['data'][0], 'ko')

            ax6 = fig.add_subplot(nrows, ncols, 6, projection=projection)
            display.plot_ppi_map('V', ele, ax=ax6, vmin=-8, vmax=8., title='Doppler Velocity',
                                 colorbar_label=radar.fields['V']['units'], cmap='pyart_BuDRd18',
                                 min_lon=radar.longitude['data'][0] - 2 * x, max_lon=radar.longitude['data'][0] + 2 * x,
                                 min_lat=radar.latitude['data'][0] - 2 * x, max_lat=radar.latitude['data'][0] + 2 * x,
                                 lon_lines=np.arange(52, 58, .4), resolution='10m',
                                 lat_lines=np.arange(15.5, 18.5, .2), projection=projection,
                                 fig=fig, lat_0=radar.latitude['data'][0],
                                 lon_0=radar.longitude['data'][0])
            display.plot_range_ring(25., line_style='k--', lw=1)
            display.plot_range_ring(50., line_style='k-', lw=0.5)
            display.plot_range_ring(75., line_style='k--', lw=1)
            display.plot_range_ring(100., line_style='k-', lw=0.5)
            display.plot_range_ring(125., line_style='k--', lw=1)
            display.plot_range_ring(150., line_style='k-', lw=0.5)
            # Indicate the radar location with a point
            display.plot_point(radar.longitude['data'][0], radar.latitude['data'][0], 'ko')

            ax7 = fig.add_subplot(nrows, ncols, 7, projection=projection)
            display.plot_ppi_map('W', ele, ax=ax7, vmin=0, vmax=5., title='Spectrum Width',
                                 colorbar_label=radar.fields['W']['units'], cmap='pyart_NWS_SPW',
                                 min_lon=radar.longitude['data'][0] - 2 * x, max_lon=radar.longitude['data'][0] + 2 * x,
                                 min_lat=radar.latitude['data'][0] - 2 * x, max_lat=radar.latitude['data'][0] + 2 * x,
                                 lon_lines=np.arange(52, 58, .4), resolution='10m',
                                 lat_lines=np.arange(15.5, 18.5, .2), projection=projection,
                                 fig=fig, lat_0=radar.latitude['data'][0],
                                 lon_0=radar.longitude['data'][0])
            display.plot_range_ring(25., line_style='k--', lw=1)
            display.plot_range_ring(50., line_style='k-', lw=0.5)
            display.plot_range_ring(75., line_style='k--', lw=1)
            display.plot_range_ring(100., line_style='k-', lw=0.5)
            display.plot_range_ring(125., line_style='k--', lw=1)
            display.plot_range_ring(150., line_style='k-', lw=0.5)
            # Indicate the radar location with a point
            display.plot_point(radar.longitude['data'][0], radar.latitude['data'][0], 'ko')

            ax8 = fig.add_subplot(nrows, ncols, 8, projection=projection)
            display.plot_ppi_map('SNR', ele, ax=ax8, title='SNR', colorbar_label=radar.fields['SNR']['units'],
                                 cmap='pyart_Carbone17',
                                 min_lon=radar.longitude['data'][0] - 2 * x, max_lon=radar.longitude['data'][0] + 2 * x,
                                 min_lat=radar.latitude['data'][0] - 2 * x, max_lat=radar.latitude['data'][0] + 2 * x,
                                 lon_lines=np.arange(52, 58, .4), resolution='10m',
                                 lat_lines=np.arange(15.5, 18.5, .2), projection=projection,
                                 fig=fig, lat_0=radar.latitude['data'][0],
                                 lon_0=radar.longitude['data'][0])
            display.plot_range_ring(25., line_style='k--', lw=1)
            display.plot_range_ring(50., line_style='k-', lw=0.5)
            display.plot_range_ring(75., line_style='k--', lw=1)
            display.plot_range_ring(100., line_style='k-', lw=0.5)
            display.plot_range_ring(125., line_style='k--', lw=1)
            display.plot_range_ring(150., line_style='k-', lw=0.5)
            # Indicate the radar location with a point
            display.plot_point(radar.longitude['data'][0], radar.latitude['data'][0], 'ko')

            ax9 = fig.add_subplot(nrows, ncols, 9, projection=projection)
            display.plot_ppi_map('SQI', ele, ax=ax9, title='SQI', colorbar_label=radar.fields['SQI']['units'],
                                 cmap='pyart_Carbone17',
                                 min_lon=radar.longitude['data'][0] - 2 * x, max_lon=radar.longitude['data'][0] + 2 * x,
                                 min_lat=radar.latitude['data'][0] - 2 * x, max_lat=radar.latitude['data'][0] + 2 * x,
                                 lon_lines=np.arange(52, 58, .4), resolution='10m',
                                 lat_lines=np.arange(15.5, 18.5, .2), projection=projection,
                                 fig=fig, lat_0=radar.latitude['data'][0],
                                 lon_0=radar.longitude['data'][0])
            display.plot_range_ring(25., line_style='k--', lw=1)
            display.plot_range_ring(50., line_style='k-', lw=0.5)
            display.plot_range_ring(75., line_style='k--', lw=1)
            display.plot_range_ring(100., line_style='k-', lw=0.5)
            display.plot_range_ring(125., line_style='k--', lw=1)
            display.plot_range_ring(150., line_style='k-', lw=0.5)
            # Indicate the radar location with a point
            display.plot_point(radar.longitude['data'][0], radar.latitude['data'][0], 'ko')

            ax10 = fig.add_subplot(nrows, ncols, 10, projection=projection)
            display.plot_ppi_map('uPhiDP', ele, vmin=-360, vmax=360., title='Unfiltered Differential Phase',
                                 colorbar_label=radar.fields['uPhiDP']['units'], cmap='pyart_Wild25',
                                 min_lon=radar.longitude['data'][0] - 2 * x, max_lon=radar.longitude['data'][0] + 2 * x,
                                 min_lat=radar.latitude['data'][0] - 2 * x, max_lat=radar.latitude['data'][0] + 2 * x,
                                 lon_lines=np.arange(52, 58, .4), resolution='10m',
                                 lat_lines=np.arange(15.5, 18.5, .2), projection=projection,
                                 fig=fig, lat_0=radar.latitude['data'][0],
                                 lon_0=radar.longitude['data'][0])
            display.plot_range_ring(25., line_style='k--', lw=1)
            display.plot_range_ring(50., line_style='k-', lw=0.5)
            display.plot_range_ring(75., line_style='k--', lw=1)
            display.plot_range_ring(100., line_style='k-', lw=0.5)
            display.plot_range_ring(125., line_style='k--', lw=1)
            display.plot_range_ring(150., line_style='k-', lw=0.5)
            # Indicate the radar location with a point
            display.plot_point(radar.longitude['data'][0], radar.latitude['data'][0], 'ko')

            plt.suptitle(title, fontsize=24)

            if not os.path.exists(fig_save_file_path):
                os.makedirs(fig_save_file_path)

            plt.savefig(fig_save_file_path + plot_file_name, dpi=100)

            plt.close()

            del radar
            del display



    data_dir = '/Volumes/Neely/PestDAR/Oman_Raw_Netcdf_Radar_Data/sur/'
    plotpath = '/Volumes/Neely/PestDAR/Oman_Raw_Data_Maps/'

    all_files=glob(data_dir+'**/*R-202006*.nc', recursive=True)

    radar = pyart.io.read(all_files[0])

    for f in all_files:
        print(f)
        for e in np.arange(0,len(radar.fixed_angle['data'])):
            try:
                plot_imd_radar(f,e,plotpath)
            except:
                print(str(f) + ' has an issue.')

if __name__ == '__main__':
    main()
