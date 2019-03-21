

from pyspark import SparkConf, SparkContext,streaming

APP_NAME = "INF553"

def mapper(line):
    return int(line)


def calculate(rdd):

    def trans(win, cur_num):
        if win.count(cur_num) == 3:
            win.remove(cur_num)
            win.remove(cur_num)
            win.append(2*cur_num)
            return trans(win, 2*cur_num)
        else:
            return sorted(win, reverse=True)

    global bit_win
    global whole_queue
    global win_size
    global the_last_bucket
    batch = rdd.map(mapper)
    cur_bits = batch.collect()
    while cur_bits:
        cur_bit = cur_bits.pop(0)
        whole_queue.append(cur_bit)
        win_size.append(cur_bit)
        if cur_bit == 1:
            bit_win.append(1)
            bit_win = trans(bit_win, 1)
    while len(win_size) >= 1000:
        the_last_bucket = bit_win[0]
        count = 0
        while count != the_last_bucket:
            cur = win_size.pop(0)
            if cur == 1:
                count += 1
        bit_win = bit_win[1:]
    if len(whole_queue) >= 1000:
        true_count = sum(whole_queue[-1000:])
        predict_count = sum(bit_win) + the_last_bucket/2
        print ('Estimate number of ones in the last 1000 bits: %s' % predict_count)
        print('Actual number of ones in the last 1000 bits: %s' % true_count)


def main(ssc):
    line = ssc.socketTextStream("localhost", 9999)
    line.foreachRDD(calculate)
    ssc.start()  # Start the computation
    ssc.awaitTermination()




if __name__ == "__main__":
    conf = SparkConf().setAppName(APP_NAME)
    conf = conf.setMaster("local[*]")
    sc   = SparkContext(conf=conf)
    sc.setLogLevel(logLevel="OFF")
    ssc  = streaming.StreamingContext(sc,10)
    whole_queue = []
    bit_win = []
    win_size = []
    the_last_bucket = 0
    # Execute Main functionality
    main(ssc)