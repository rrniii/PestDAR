def main():
    import matplotlib.pyplot as plt
    import pyart
    import netCDF4
    from glob import glob
    import os
    import numpy as np


    def plot_imd_radar(fpath, ele, R, plotpath):
        # Plotting Options Set in Function
        # ele = 0 #Elevation
        # R = 50#  #Min and Mac Range from Radar in km

        # Read Files and Setup Plotting
        radar = pyart.io.read_sigmet(fpath)
        display = pyart.graph.RadarDisplay(radar)

        # set the figure title and show
        instrument_name = radar.metadata['instrument_name'].decode('utf-8')
        time_start = netCDF4.num2date(radar.time['data'][0], radar.time['units'])
        time_text = ' ' + time_start.strftime('%Y-%m-%d %H:%M:%SZ')

        # retrieve elevation information and make a string for title.
        elevation = radar.fixed_angle['data'][ele]
        ele_text = '%0.1f' % (elevation)

        #make title.
        title = instrument_name + time_text + ' Elevation %.1f' % (elevation)

        #make folder name.
        if np.round(elevation, 0) > 9.99:
            ele_folder = 'ele' + ele_text[0] + ele_text[1] + '_' + ele_text[3] + '/'
            ele_name = 'ele' + ele_text[0] + ele_text[1] + '_' + ele_text[3]
        else:
            ele_folder = 'ele' + ele_text[0] + '_' + ele_text[2] + '/'
            ele_name = 'ele' + ele_text[0] + '_' + ele_text[2]

        plot_file_name = instrument_name + '_' + time_start.strftime('%Y-%m-%dT%H%M%SZ') + ele_name + '.png'

        loc_folder = instrument_name + '/'

        R_folder = str(R) + 'km' + '/'

        #use information above to make full plot save path organised by radar location, elevation and maximum range
        fig_save_file_path = plotpath + loc_folder + ele_folder + R_folder

        # Figure Options
        width = 30  # in inches
        height = 10  # in inches

        fig = plt.figure(figsize=(width, height))
        nrows = 2
        ncols = 5

        #plotting
        ax1 = fig.add_subplot(nrows, ncols, 1)
        display.plot('reflectivity', ele, ax=ax1, vmin=-32, vmax=64., title='Horizontal Reflectivity',
                     colorbar_label=radar.fields['reflectivity']['units'],
                     axislabels=('', 'North South distance from radar (km)'))
        display.set_limits((-R, R), (-R, R), ax=ax1)

        ax2 = fig.add_subplot(nrows, ncols, 2)
        display.plot('differential_reflectivity', ele, ax=ax2, vmin=-2, vmax=10., title='Differential Reflectivity',
                     colorbar_label=radar.fields['differential_reflectivity']['units'],
                     axislabels=('', ''), cmap='pyart_RefDiff')
        display.set_limits((-R, R), (-R, R), ax=ax2)

        ax3 = fig.add_subplot(nrows, ncols, 3)
        display.plot('cross_correlation_ratio', ele, ax=ax3, vmin=0, vmax=1., title='Cross Correlation Ratio',
                     colorbar_label=radar.fields['cross_correlation_ratio']['units'],
                     axislabels=('', ''), cmap='pyart_RefDiff')
        display.set_limits((-R, R), (-R, R), ax=ax3)

        ax4 = fig.add_subplot(nrows, ncols, 4)
        display.plot('specific_differential_phase', ele, ax=ax4, vmin=-0.5, vmax=2.,
                     title='Specific Differential Phase',
                     colorbar_label=radar.fields['specific_differential_phase']['units'],
                     axislabels=('', ''), cmap='pyart_Theodore16')
        display.set_limits((-R, R), (-R, R), ax=ax4)

        ax5 = fig.add_subplot(nrows, ncols, 5)
        display.plot('differential_phase', ele, ax=ax5, vmin=0, vmax=180., title='Differential Phase',
                     colorbar_label=radar.fields['differential_phase']['units'],
                     axislabels=('', ''), cmap='pyart_Wild25')
        display.set_limits((-R, R), (-R, R), ax=ax5)

        ax6 = fig.add_subplot(nrows, ncols, 6)
        display.plot('velocity', ele, ax=ax6, vmin=-16, vmax=16., title='Doppler Velocity',
                     colorbar_label=radar.fields['velocity']['units'],
                     axislabels=('East West distance from radar (km)', 'North South distance from radar (km)'),
                     cmap='pyart_BuDRd18')
        display.set_limits((-R, R), (-R, R), ax=ax6)

        ax7 = fig.add_subplot(nrows, ncols, 7)
        display.plot('spectrum_width', ele, ax=ax7, vmin=0, vmax=5., title='Spectrum Width',
                     colorbar_label=radar.fields['spectrum_width']['units'],
                     axislabels=('East West distance from radar (km)', ''), cmap='pyart_NWS_SPW')
        display.set_limits((-R, R), (-R, R), ax=ax7)

        ax8 = fig.add_subplot(nrows, ncols, 8)
        display.plot('radar_echo_classification', ele, ax=ax8, title='Radar Echo Classification',
                     colorbar_label=radar.fields['radar_echo_classification']['units'],
                     axislabels=('East West distance from radar (km)', ''), cmap='Accent')
        display.set_limits((-R, R), (-R, R), ax=ax8)

        ax9 = fig.add_subplot(nrows, ncols, 9)
        display.plot('normalized_coherent_power', ele, ax=ax9, title='Normalized Coherent Power',
                     colorbar_label=radar.fields['normalized_coherent_power']['units'],
                     axislabels=('East West distance from radar (km)', ''), cmap='pyart_Carbone17')
        display.set_limits((-R, R), (-R, R), ax=ax9)

        ax10 = fig.add_subplot(nrows, ncols, 10)
        display.plot('total_power', ele, ax=ax10, vmin=-32, vmax=64., title='Total Power',
                     colorbar_label=radar.fields['total_power']['units'],
                     axislabels=('East West distance from radar (km)', ''), cmap='pyart_Carbone17')
        display.set_limits((-R, R), (-R, R), ax=ax10)

        display.plot_cross_hair(3.)
        plt.suptitle(title, fontsize=24)

        if not os.path.exists(fig_save_file_path):
            os.makedirs(fig_save_file_path)

        plt.savefig(fig_save_file_path + plot_file_name, dpi=100)

        plt.close()

        del fig
        del radar
        del display



    data_dir='/Volumes/Neely/PestDAR/Indian_Raw_Radar_Data/' # Location of all the data
    plotpath='/Volumes/Neely/PestDAR/Indian_Raw_Radar_Data_Plots/' # where you want to put the plots

    all_files=glob(data_dir+ '*RAW*') #gets list of all data files.

    radar=pyart.io.read_sigmet(all_files[0]) # loads the first data file to get some information for plotting.

    #rge=[25,50,75,100,125,150,175,200,225,250] #select the different maximum ranges you want to plot in km

    rge = [25,50,75,100]

    for f in all_files: #loop through files
        print(f) # print file name
        print(radar.fixed_angle['data'])

        for e in np.arange(0,len(radar.fixed_angle['data'])):  #loop through all angles
            for r in rge: #loop thorugh the maximum ranges you want to plot
                try: # try plotting.
                    plot_imd_radar(f,e,r,plotpath) #mkae a plot for the file, elevation angle and maximum range you select.
                except:
                    print(str(f) + ' has an issue.') #If the plotting does not work, let me know.

if __name__ == '__main__':
    main()
