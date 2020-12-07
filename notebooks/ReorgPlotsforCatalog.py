def main():
    from glob import glob
    import os
    import datetime
    import shutil

    def plot_imd_radar(top_level_dir):
        #elevation_dirs
        elevation_dirs=glob(top_level_dir+'/ele*',recursive=False)
        print(elevation_dirs)

        #range_dirs
        range_dirs=[]
        for d in elevation_dirs:
            range_dirs.extend(glob(d+'/*km',recursive=False))

        print(range_dirs)

        range_dirs=elevation_dirs

        for r in range_dirs:
            print(r)
            #all files in one dir sorted
            all_files=sorted(glob(r+'/*.png',recursive=False))
            first_day = all_files[0][-28:-18]
            if first_day[-1] == "T":
                first_day = all_files[0][-29:-19]
            print(first_day)

            last_day = all_files[-1][-28:-18]
            if last_day[-1] == "T":
                last_day = all_files[-1][-29:-19]
            print(last_day)

            start = datetime.datetime.strptime(str(first_day), "%Y-%m-%d")
            end = datetime.datetime.strptime(str(last_day), "%Y-%m-%d")
            date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days+1)]

            for date in date_generated:
                day_files=sorted(glob(r+'/*'+date.strftime("%Y-%m-%d")+'*.png',recursive=False))
                print(date.strftime("%Y-%m-%d"))
                day_dir=os.path.join(r,date.strftime("%Y-%m-%d"))
                os.mkdir(day_dir)
                print(day_dir)
                for f in day_files:
                    shutil.move(f, day_dir)



    top_level_dir='/Volumes/Neely/PestDAR/Oman_Raw_Data_Maps/Salalah/'
    plot_imd_radar(top_level_dir)

if __name__ == '__main__':
    main()