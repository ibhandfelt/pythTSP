import pickle
import sys
import traceback


def main(argv):
    nm = 10

    if len(argv) >= 3 and argv[0]:
        nm = int(argv[0])

    if nm <= 10:
        na = 20
        ni = 12
        nr = 1
    else:
        na = 28
        ni = 20
        nr = 1

    stuff = pickle.load(open(argv[1], "r"))
    cities = stuff[0]
    cm = stuff[1]
    # why are we doing this?
    if nm < len(cm):
        cm = cm[0:nm]
        for i in range(0, nm):
            cm[i] = cm[i][0:nm]



    try:
        graph = GraphBit(nm, cm)
        bpv = None
        bpc = sys.maxint
        for i in range(0, nr):
            print "Repetition %s" % i
            graph.reset_tau()
            workers = BigGroup(graph, na, ni)
            print "Colony Started"
            workers.start()
            if workers.bpc < bpc:
                print "Colony Path"
                bpv = workers.bpv
                bpc = workers.bpc

        print "\n------------------------------------------------------------"
        print "                     Results                                "
        print "------------------------------------------------------------"
        print "\nBest path = %s" % (bpv,)
        city_vec = []
        for node in bpv:
            print cities[node] + " ",
            city_vec.append(cities[node])
        print "\nBest path cost = %s\n" % (bpc,)
        results = [bpv, city_vec, bpc]
        pickle.dump(results, open(argv[2], 'w+'))
    except Exception, e:
        print "exception: " + str(e)
        traceback.print_exc()


if __name__ == "__main__":
    main(sys.argv[1:])    

