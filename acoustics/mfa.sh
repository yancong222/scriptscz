for filename in /Users/xyz/* ; # optional
do
    justfile=$(basename -- "$filename") # optional
    uid="${justfile%.*}" # optional

    mfa align /path/to/librispeech/dataset /path/to/librispeech/lexicon.txt english~/Documents/aligned_librispeech ;
done ;
