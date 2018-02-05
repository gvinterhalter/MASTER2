PATH="~/Installed/neo4j/bin:$PATH"

name="go.db"

neo4j stop

rm -fr  ~/Installed/neo4j/data/databases/$name
echo \
------------------------------------------------------------------------------

neo4j-admin import \
     --database        $name          \
     --nodes           go_term.csv    \
     --nodes           keyw.csv       \
     --nodes           seq.csv       \
     --relationships   go_relations.csv    \
     --relationships   keyw_rel.csv   \
     --relationships   seq_relations.csv

neo4j start 
echo \
------------------------------------------------------------------------------

n=5
while [ $n -gt 0 ]
do
  echo "sleeping $n seconds"
  sleep 1
  n=`expr $n - 1`
done
echo \
------------------------------------------------------------------------------

echo "runing cypher:"
cat make.cypher
echo \
------------------------------------------------------------------------------

cypher-shell -u neo4j -p 124  < make.cypher
