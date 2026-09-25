from datetime import datetime
import time
import matplotlib.pyplot as plt
import pickle
import multiprocessing

def create_short_baker(m):
    save_filepath = "baked_animations_cache.pkl"
    with open(save_filepath, "rb") as f:
        loaded_data = pickle.load(f)
    
    new_data = dict({})
    l = list(loaded_data)
    for i in range(len(loaded_data)):
        if i < m:
            sample = l[i]
            new_data[sample] = loaded_data[sample]
            
    with open("save.pkl", "wb") as f:
        pickle.dump(new_data, f)

# Η συνάρτηση αυτή θα τρέχει σε δικό της αυτόνομο process
def open_file_isolated(return_dict, process_id):
    import gc
    gc.collect() # Καθαρίζουμε τον Garbage Collector για σιγουριά

    t = time.perf_counter()
    with open("save.pkl","rb") as f:
        c = pickle.load(f)
    t_end = time.perf_counter()
    
    # Αποθηκεύουμε το αποτέλεσμα στο κοινόχρηστο λεξικό
    return_dict[process_id] = (t_end - t)


def run():
    t_results = []
    numbers = [i+1 for i in range(201)]

    # Απαραίτητο για τα Windows όταν χρησιμοποιούμε multiprocessing
    manager = multiprocessing.Manager() 
    return_dict = manager.dict()

    for i in range(201):
        print(f"Δημιουργία δεδομένων για n={i+1}")
        create_short_baker(i + 1)
        
        print(f"Μέτρηση χρόνου ανάγνωσης για n={i+1} σε νέο process")
        # Φτιάχνουμε ένα νέο Process που θα τρέξει την open_file_isolated
        p = multiprocessing.Process(target=open_file_isolated, args=(return_dict, i))
        p.start()
        p.join() # Περιμένουμε να τελειώσει το process

        t_results.append(return_dict[i])
        print(f"Χρόνος: {return_dict[i]:.6f} seconds\n")

    plt.plot(numbers, t_results, "-o")
    plt.xlabel("Αριθμός Animations")
    plt.ylabel("Χρόνος Φόρτωσης (δευτερόλεπτα)")
    plt.title("Πραγματικός Χρόνος Φόρτωσης (Isolated Processes)")
    plt.show()

if __name__ == '__main__':
    run()