You need to extract the relevant information from the AMI corpus in CSV format. The AMI is distributed in NXT format which is difficult to handle with python.

Download the AMI corpus here: http://groups.inf.ed.ac.uk/ami/download/

And the NXT toolkit here: http://groups.inf.ed.ac.uk/nxt/

You might need to adjust the java classpath:
- export NXT="nxt_1.4.4/"
- export CLASSPATH=".:$NXT/lib:$NXT/lib/nxt.jar:$NXT/lib/jdom.jar:$NXT/lib/xalan.jar:$NXT/lib/xercesImpl.jar:$NXT/lib/xml-apis.jar" 

The following command extracts the required data from the meeting $OBS and saves it to ./csv/$OBS-trans.csv (e.g. OBS=ES2002a)

java FunctionQuery -corpus ./ami_public_manual_1.6/AMI-metadata.xml -observation "$OBS" -q '($d dact) ($t da-type): $d > $t' -atts '$t@name' '@extract(($ap adjacency-pair) ($at ap-type): $ap > $at & $ap >"target" $d, $at@name, 0)' '$d@who' '$d' '@count(($f dsfl) ($ft dsfl-type): $f > $ft & $f > $d & ! $ft@name=="reparandum" & ! $ft@name=="dm")' > "csv/$OBS-trans.csv" 2> /dev/null

This represents every utterance in $OBS as a comma-separated list of:
- the timestamp of the utterance
- the speech act type of the utterance
- IF the utterances is second-part of an adjacency pair, the type of adjacency; otherwise -
- IF the utterance is second-part of an adjacency pair, the timestamp of the first part; otherwise -
- the speaker
- the utterance's surface form

Then you can run the tools in ami-tools.py.

- getCorpus() assembles the CSV files extracted above as a dictionary of lists. The keys of the dictionary are the names of the observations.
- getTurn(observation,i) takes a list observation and an integer i and finds the dialogue turn that the utterance i appears in.
- findTarget(observation,i) takes a list observation and an integer i. If the utterance at i is the second-part of an adjacency pair, return the index of the first-part. Otherwise return i.
