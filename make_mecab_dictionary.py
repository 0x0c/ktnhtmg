# -*- encoding: utf-8 -*-
import sys
import codecs

if __name__ == "__main__":
        argvs = sys.argv
        argc = len(argvs)
        if (argc != 3):
                print 'Usage: # python %s Input_FileName Output_FileName' % argvs[0]
                quit()

        fin_name = argvs[1]
        fout_name = argvs[2]

        # fin = codecs.open(fin_name, "r", "utf-8")
        fin = open(fin_name, "r")
        # fout = codecs.open(fout_name, "w", "utf-8")
        fout = open(fout_name, "w")
        for line in fin:
                #word = line[:-1].split('\t')[1]
                line = line.replace('\n','')
                line = line.replace('\r','')
                word = line.split(',')
                print word[0] + word[1]
                cost = int(max(-36000, -400*len(word[0])**1.5))
                # fout.write(u"%s,-1,-1,%d,名詞,一般,*,*,*,*,*,*,%s,%s\n" % (word[0], cost, word[1], word[1]))
                print >> fout, word[0]+",-1,-1,"+str(cost)+",名詞,一般,*,*,*,*,*,*,"+word[1]+","+word[1]
        fin.close()
        fout.close()