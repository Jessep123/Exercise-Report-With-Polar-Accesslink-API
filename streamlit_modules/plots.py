#Function to plot total time spent in each training zone in a pie chart
def visualize_zone_times(data):
    import matplotlib.pyplot as plt

    #Reducing data to zone values
    data = data[['1', '2', '3', '4', '5']]

    #Calculating sum of zone values for data
    values = data.sum()

    #Filtering out any values of 0
    filtered_values = values[values != 0]

    #More accurate labels for plot based on training zones
    labels_mapping = {'1': 'UT4', '2':'UT3', '3':'UT2', '4':'UT1', '5':'AT'}

    #List of labels based on non-zero values 
    labels = [labels_mapping[key] for key in filtered_values.index]

#     #Colour dictionary based on training zone labels
    col_dic = {'UT4': '#A9A9A9', 'UT3': "#0B9AE7", 'UT2': "#23A70F", 'UT1': "#DD8518", 'AT': "#D50202" }
    
    fig, ax = plt.subplots()

    #Function to display percentage and total values
    def make_autopct(values):
        def my_autopct(pct):
            def convert_to_time(seconds):
                min, sec = divmod(seconds, 60)
                hour, min = divmod(min, 60)
                return '%d:%02d:%02d' % (hour, min, sec)
            
            total = sum(values)

            val = int(round(pct*total/100.0))
            
            return '{p:.2f}% ({v})'.format(p=pct,v=convert_to_time(val))
        return my_autopct

    #Explode to space all wedges apart a bit more
    explosion = [0.05 for value in range(len(filtered_values))]

    #Plotting  values
    ax.pie(filtered_values, 
           colors= [col_dic[key] for key in labels], 
           autopct=make_autopct(filtered_values),
           explode = explosion,
        #    shadow=True
        )
    
    ax.legend(labels)

    return fig



def activity_line_graph_hr(data):
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    import math

    hr = data["hr"].iloc[0]
    hr = np.array(hr)

    x = np.arange(len(hr))

    # Create segments
    points = np.array([x, hr]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Define color rules
    def get_color(val):
        if val < 119:
            return "#A9A9A9"  # UT4
        elif val <= 139:
            return "#0B9AE7"  # UT3
        elif val <= 158:
            return "#23A70F"  # UT2
        elif val <= 178:
            return "#DD8518"  # UT1
        else:
            return "#D50202"  # AT

    colors = [get_color(v) for v in hr[:-1]]

    fig, ax = plt.subplots()

    lc = LineCollection(segments, colors=colors, linewidth=1.5)
    ax.add_collection(lc)

    
    #Formatting x axis
    ax.set_xlim(x.min(), x.max())

    # mins = math.ceil((len(hr)/60) / 15)

    # ax.set_xticks([number * 1800 for number in range(mins + 1)])

    # ax.set_xticklabels([number * 15 for number in range(mins + 1)])

    ax.set_xlabel('Time (Mins)')

    #Formatting y axis
    ax.set_ylim(hr.min(), 200)
    ax.set_ylabel('Heartrate (bpm)')


    return fig

