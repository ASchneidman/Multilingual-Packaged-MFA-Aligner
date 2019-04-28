import sys,os,json,re
import tgt

def process_intervals(file_startime,intervals):
    tuples = []
    for interval in intervals:
        tuples.append(((file_startime + interval.start_time,
                        file_startime + interval.end_time),
                        interval.text))
    return tuples

def get_tuples(aligned_dir):
    textgrids = [f for f in os.listdir(aligned_dir) if ".TextGrid" in f]

    all_tuples_words = []
    all_tuples_phones = []

    for textgrid in textgrids:
        file_startime = float(textgrid[:textgrid.index("_")]) / 1000.0

        textgrid_obj = tgt.io.read_textgrid(os.path.join(aligned_dir,textgrid))

        word_intervals = None
        phone_intervals = None

        try:
            word_intervals = textgrid_obj.tiers[0]
            phone_intervals = textgrid_obj.tiers[1]
        except Exception as e:
            print("Failed to extract tiers: %s" % (str(e)))

        word_interval_tuples = process_intervals(file_startime,word_intervals.intervals)
        phone_interval_tuples = process_intervals(file_startime,phone_intervals.intervals)

        all_tuples_words.extend(word_interval_tuples)
        all_tuples_phones.extend(phone_interval_tuples)

    all_tuples_words = sorted(all_tuples_words,key=lambda x:x[0][0])
    all_tuples_phones = sorted(all_tuples_phones,key=lambda x:x[0][0])
    return all_tuples_words,all_tuples_phones

if __name__ == '__main__':
    print(get_tuples(sys.argv[1]))
