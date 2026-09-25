import matplotlib.pyplot as plt
import numpy as np
import pickle

def show_each_one(n):

    for i in range(n):
        with open(f"times_manual_{i+1}.pkl","rb") as f:
            times = pickle.load(f)
        f.close()

        all_time = times[-1].total_seconds()
        times = times[0:(len(times)-1)]

        times = [k.total_seconds() for k in times]

        times = np.array(times)
        x = [j+1 for j in range(len(times))]
        x = np.array(x)

        print(f"All time: {all_time}")
        print(f"Average time: {sum(times)/len(times)}")
        print(f"Time on other endevors: {all_time-sum(times)}")

        plt.plot(x,times)
        plt.show()


def show_all_together(n):
    all_times = []
    all_x = []

    sinolika_times = []
    all_time_other = []

    
    for i in range(n):
        with open(f"times_manual_{i+1}.pkl","rb") as f:
            times = pickle.load(f)
        f.close()

        all_time = times[-1].total_seconds()
        times = times[0:(len(times)-1)]

        times = [k.total_seconds() for k in times]

        sinolika_times.append(all_time)
        all_time_other.append(all_time-sum(times))

        all_times += times
        x = [j +1 for j in range(len(times))]
        all_x += x

    s = sum(all_times)/len(all_times)
    for i in range(len(all_times)):
        try:
            t = all_times[i]
            if t > 5*s:
                print(t)
                all_times.pop(i)
                all_x.pop(i)
        except:
            continue
    all_time = np.array(all_time)
    all_x = np.array(all_x)

    print(f"Average all time: {sum(sinolika_times)/len(sinolika_times)}")
    print(f"Average time: {s}")
    print(f"Average time on other endevors: {sum(all_time_other)/len(all_time_other)}")

    plt.plot(all_x,all_times,"o")
    plt.show()


def create_short_baker():

    save_filepath = "baked_animations_cache.pkl"

    with open(save_filepath, "rb") as f:
        loaded_data = pickle.load(f)
    f.close()

    new_data = dict({})
    l = list(loaded_data)

    print(l.index("27_MYTILINH_calendar_1"))

    for i in range(len(loaded_data)):

        if i < 25 or i > 170:
            sample = l[i]
            print(sample,type(new_data),type(loaded_data))
            new_data[sample] = loaded_data[sample]

    with open("short_baked_animations_cache.pkl", "wb") as f:
        pickle.dump(new_data, f)
    f.close()

#create_short_baker()

show_each_one(6)
#show_all_together(6)