wget http://hgdownload.cse.ucsc.edu/goldenpath/hg19/bigZips/chromFa.tar.gz
tar -xf chromFa.tar.gz
for f in *.fa; do tail -n +2 $f | tr --delete '\n' > ${f%%.*}.txt; done