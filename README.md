Large Scale Entity Linking
The first assignment for this course is to perform Entity Linking on a collection of web pages using entities from Freebase. Your solution should be scalable and accurate, and conform to the specifications below. You should work in groups of 4 people. You can use any existing languages or tools you want, as long as it's easy for us to run it on the DAS-4 cluster. Of course, your solution is not allowed to call web services over the internet. You are encouraged to use the technologies covered in the lectures.

Your program should receive in input a gzipped WARC file, and returns in output a three-column tab-separated file with document IDs (i.e., the content of the field 'WARC-Record-ID'), entity surface forms (like "Berlin"), and Freebase entity IDs (like "/m/03hrz"). There is a sample file of the input (warc) and output (tsv) formats in the data directory. Your program must be runnable on the DAS-4 cluster using a bash script, and you should provide a README file with a description of your approach. For example, your program could be run using the command bash run.sh input.warc.gz > output.tsv.

The performance of your solution will be graded on three dimensions: Compliance (20%), scalability (20%) and quality (60%).

Compliance
Does the program that you deliver complies with the specifications of the assignment? To measure this aspect, we will evaluate to what extent your program can be run easily on the DAS-4 and whether it produces the output as specified above. Points will be detracted if your program does not compile, if it requires extensive and elaborate installation procedures, whether it produces the output in an incorrect format, etc.

Scalability
Your solution should be able to be executed on large volumes of data. You can improve the scalability either by using frameworks like Spark to parallelize the computation, and/or by avoiding to use very complex algorithms that are very slow. To measure this aspect, we will evaluate whether you make use of big data frameworks, and test how fast your algorithm can disambiguate some example web pages.

Quality
Your solution should be able to correctly disambiguate as many entities as possible. To measure the quality of your solution, we will use the F1 score on some test webpages (these webpages are not available to the students).

Starting code
To help you with the development of the assignment, we provide some example Python code in the directory "/home/jurbani/wdps/" in the DAS-4 cluster. This code is also available here. Note that you do not have to write your program in Python. As mentioned above, you can use whatever language you want.

We have loaded four major KBs into a triple store called "Trident". The KBs are Freebase, YAGO, Wikidata, and DBPedia. You can access these KBs with SPARQL queries. To start the triple store, you can use the script "start_sparql_server.sh". This script will start the triple store in a node so that you can query it (if you want) during the disambiguation process. In principle, the triple store can be accessed with a command like : curl -XPOST -s 'http://<host>:8082/sparql' -d "print=true&query=SELECT * WHERE { ?s ?p ?o . } LIMIT 10". To experiment with some SPARQL examples, see https://query.wikidata.org/ . Both services return JSON. Because Freebase was integrated into the Google Knowledge Graph, you can look up IDs on Google using URLs like this: [http://g.co/kg/m/03hrz].

In order to facilitate syntactic matching between the entities in the webpage and the ones in the KB, we indexed all the Freebase labels in Elasticsearch. With this program, you can retrieve all the entities IDs that match a given string. The elasticsearch server can be started on a DAS-4 node with the commands shown in the file start_elasticsearch_server.sh. Once the server is started, it can be accessed from the command line like this: curl "http://<host>:9200/freebase/label/_search?q=obama" .
