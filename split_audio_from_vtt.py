from pydub import AudioSegment
import sys, time, re, os

def time_to_millisec(time_seg):
    time_seg = time_seg.replace("\n","")
    no_frac, frac = time_seg.split(".")

    struct_time = time.strptime(no_frac, "%H:%M:%S")

    hour = struct_time.tm_hour
    minute = struct_time.tm_min
    second = struct_time.tm_sec + (int(frac) / 1000)


    millisec = (hour * 3.6e6) + (minute * 60000) + (second * 1000)
    return millisec

# Returns list of 2tuples where each tuple is a segment of the transcript
def get_segments(vtt):
    segments = []

    f = open(vtt,"r")
    # Cut off descriptor lines
    lines = f.readlines()
    lines = lines[4:]
    lines = [l for l in lines if l != '\n']

    for i in range(len(lines)):
        # If even, its a time interval
        #if (i % 2 == 0):
        if (re.match('''\d\d:\d\d:\d\d\.\d\d\d --> \d\d:\d\d:\d\d\.\d\d\d''',lines[i])):
            interval = lines[i]
            initial = interval[:12]
            end = interval[17:]
            text = ''
            j = i+1
            while (j < len(lines) and (not re.match('''\d\d:\d\d:\d\d\.\d\d\d --> \d\d:\d\d:\d\d\.\d\d\d''',lines[j]))):
                text += lines[j].replace('\n', ' ')
                j += 1

            initial_millisecond = time_to_millisec(initial)
            end_millisecond = time_to_millisec(end)

            segments.append((initial_millisecond,end_millisecond,text))
    f.close()
    return segments

def create_textgrid(start_milliseconds,end_milliseconds,segment_name, text):
    textgrid = open(segment_name,"w")
    total_time = end_milliseconds - start_milliseconds
    # Write preamble
    textgrid.write("File type = \"ooTextFile\"" + '\n')
    textgrid.write("Object class = \"TextGrid\""+ '\n')
    textgrid.write('\n')
    textgrid.write("xmin = 0"+ '\n')
    textgrid.write("xmax = " + str(total_time / 1000)+ '\n')
    textgrid.write("tiers? <exists>"+ '\n')
    textgrid.write("size = 1"+ '\n')
    textgrid.write("item []: "+ '\n')
    textgrid.write("    item [1]:"+ '\n')
    textgrid.write("        class = \"IntervalTier\""+ '\n')
    textgrid.write("        name = \"silences\""+ '\n')
    textgrid.write("        xmin = 0"+ '\n')
    textgrid.write("        xmax = " + str(total_time / 1000)+ '\n')
    textgrid.write("        intervals: size = " + str(1) +'\n')

    textgrid.write("        intervals [" + str(1) + "]:" + "\n")
    textgrid.write("            xmin = " + str(0) + "\n")
    textgrid.write("            xmax = " + str(total_time / 1000) + "\n")
    textgrid.write("            text = \"" + text.replace("\n","") + "\" \n")
    textgrid.close()

def make_corpus(wav, vtt, output_corpus):
    wav_name = wav.replace(".wav","")
    audio = AudioSegment.from_wav(wav)

    try:
        os.mkdir(output_corpus)
    except Exception as e:
        print("dir already exists")

    segments = get_segments(vtt)

    segment_num = 0
    max_seg = -1.0
    for (initial, end, text) in segments:
        if (initial < max_seg):
            raise Exception("init less max seg")
        max_seg = initial
        wav_segment = audio[initial:end]
        segment_name = os.path.join(output_corpus,str(initial) + "_" + str(end) + ".wav")
        #segment_name = os.path.join(output_corpus,segment_name)
        # Export wav segment
        wav_segment.export(segment_name,format="wav")
        textgrid_name = segment_name.replace(".wav",".TextGrid")
        # Create corresponding TextGrid file
        create_textgrid(initial,end,textgrid_name, text)

        lab_name = segment_name.replace(".wav",".lab")
        # Create corresponding .lab file
        lab = open(lab_name,"w")
        lab.write(text)
        lab.close()

        segment_num += 1

if __name__ == '__main__':
    make_corpus(sys.argv[1],sys.argv[2],sys.argv[3])
