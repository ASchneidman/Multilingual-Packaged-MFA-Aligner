from download import *
from split_audio_from_vtt import make_corpus
import os,sys
import subprocess
from corpus_to_tuples import get_tuples
import h5py
import numpy as np

MFA_ALIGNER = '../montreal-forced-aligner/bin/'
G2P_MODEL = 'spanish_g2p.zip'
LANG_MODEL = 'spanish.zip'

def output_h5py(intervals, work_dir, video_id, name):
    data = {}
    data[video_id] = {}
    data[video_id]['intervals'] = np.array([[a[0][0], a[0][1]] for a in intervals])
    data[video_id]['features'] = np.array([[a[1].encode('utf-8')] for a in intervals],dtype="a32")

    write5Handle=h5py.File(os.path.join(work_dir, video_id + "_" + name + ".h5py"),'w')

    vidHandle=write5Handle.create_group(video_id)
    vidHandle.create_dataset("features",data=data[video_id]["features"])
    vidHandle.create_dataset("intervals",data=data[video_id]["intervals"])
    write5Handle.close()

def align(video_id,lang):
    os.mkdir(video_id)
    work_dir = video_id
    dwnld(video_id, work_dir)

    transcription = os.path.join(work_dir,video_id + '.' + lang + '.vtt')
    wav = os.path.join(work_dir,video_id + '.wav')
    unaligned = os.path.join(work_dir,video_id + '_unaligned')
    make_corpus(wav,transcription,unaligned)
    corpus = unaligned
    video_dict = os.path.join(work_dir,video_id + '_dict.txt')

    # generate dictionary
    subprocess.check_call(MFA_ALIGNER + 'mfa_generate_dictionary ' + G2P_MODEL + ' ' + corpus + ' ' + video_dict,shell=True)

    output_dir = os.path.join(work_dir,video_id + '_aligned')
    align_call = MFA_ALIGNER + 'mfa_align ' + corpus + ' ' + video_dict + ' ' + LANG_MODEL + ' ' + output_dir
    subprocess.check_call(align_call,shell=True)

    word_intervals,phone_intervals = get_tuples(output_dir)

    output_h5py(word_intervals, work_dir, video_id, "words")
    output_h5py(word_intervals, work_dir, video_id, "phones")

    print(word_intervals)


if __name__ == '__main__':
    align(sys.argv[1],sys.argv[2])
