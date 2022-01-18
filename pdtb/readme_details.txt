1. use safari to download WordNet-3.0
	1a. https://wordnet.princeton.edu/download/current-version
	1b. move WordNet-3.0 under /2Taggers/
	1c. unzip it
2. configure WordNet-3.0
	2a. /Users/yancong/Desktop/pdtb/2Taggers/WordNet-3.0
	2b. run configure.exe on terminal [either right click and drag it to terminal, or open it with terminal]
	2c. open /2Taggers/config/file_properties.xml with vscode
	2d. go to line 41, change dictionary_path to 'Users/yancong/Desktop/pdtb/2Taggers/WordNet-3.0/dict'
3. update configuration files
	3a. go to /Users/yancong/Desktop/pdtb/2Taggers/config/properties
	3b. change wordPairsDir to '/Users/yancong/Desktop/pdtb/2Taggers/wordpairs/gigaword/content_word_pairs_stemmed_tfidf_adj_culled'

4. parse a single document
	4a. cd to /2Taggers/
	4b. java -Xmx8G -cp "bin:lib/*" discourse.tagger.app.DiscourseTaggingRunner tmp/alabama tmp/alabama.dp
	4c. here 'alabama' can be replaced by target input txt file
	4d. input file: make a copy of /2Taggers/tmp/alabama, then rename it, one sentence per line, space in btw (optional)

