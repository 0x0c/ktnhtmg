#!/usr/bin/env python

import os
import os.path
import commands

if not os.path.exists("/usr/local/Cellar/mecab-ipadic/2.7.0-20070801/lib/mecab/dic/ipadic"):
	print "[ktnhtmg Convert Script Error] : Check your ipadic directory."
	exit()
check = commands.getoutput("python make_mecab_dictionary.py list.txt list.csv")
check = commands.getoutput("/usr/local/Cellar/mecab/0.996/libexec/mecab/mecab-dict-index -d /usr/local/Cellar/mecab-ipadic/2.7.0-20070801/lib/mecab/dic/ipadic -u ./list.dic -f utf-8 -t utf-8 ./list.csv")
check = commands.getoutput("rm -rf ./result/*")
check = commands.getoutput("python dictionary_maker.py")
check = commands.getoutput("ls result")
ls = check.split("\n")
idx = 0
print commands.getoutput("pwd")
for x in xrange(0, len(ls)):
	print "./sandbox/mkdfa.pl ./result/" + str(idx)
	result = commands.getoutput("./sandbox/mkdfa.pl ./result/" + str(idx) + "/" + str(idx))
	print result
	idx += 1

if not os.path.isdir("./result"):
	os.mkdir("result")
	
run_script = open("./result/run.sh", "w")
gramlist_file = open("./result/gramlist_file", "w")
# gram = []
for x in ls:
	print >> gramlist_file, str(x + "/" + x)
	# gram.append(str(x + "/" + x))
print >> run_script, "./dependencies/dictation-kit/bin/osx/julius -gramlist ./result/gramlist_file", "-C ./dependencies/grammar-kit/hmm_mono.jconf", "-input mic"

run_script = open("./result/run_module_mode.sh", "w")
print >> run_script, "./dependencies/dictation-kit/bin/osx/julius -gramlist ./result/gramlist_file", "-C ./dependencies/grammar-kit/hmm_mono.jconf", "-input mic", "-module"

commands.getoutput("chmod +x ./result/run.sh")
commands.getoutput("chmod +x ./result/run_module_mode.sh")
