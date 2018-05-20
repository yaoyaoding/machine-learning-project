iter = 400
lr = 1
dim = 1,1,8
method = mcmc
data_dir = ./libfm_data/v2/
xdata_dir = ./libfm_data/v4/
other = -init_stdev 1 

meta = -meta $(data_dir)groups.meta
parameters = -iter $(iter) -dim $(dim) -method $(method) $(other)

hello:
	echo "Hello, Darrell!"

xlearn:
	./scripts/xlearn_train.py $(xdata_dir)combine.tsv.libfm $(xdata_dir)train.tsv.libfm $(xdata_dir)valid.tsv.libfm $(xdata_dir)test.tsv.libfm 
	./scripts/prediction_to_format_csv.py ../data/test.tsv ./xprediction.txt ./xprediction.csv

data:
	./scripts/tsv_to_libfm.py 4 ../data/combine.tsv ../data/train.tsv ../data/valid.tsv ../data/test.tsv ../data/feature.txt

valid:
	./bin/libFM -task r $(parameters) -train $(data_dir)train.tsv.libfm $(meta) -test $(data_dir)valid.tsv.libfm -out ./prediction$(index).txt 

train:
	./bin/libFM -task r $(parameters) -train $(data_dir)combine.tsv.libfm $(meta) -test $(data_dir)test.tsv.libfm -out ./prediction$(index).txt 
	./scripts/prediction_to_format_csv.py ../data/test.tsv ./prediction$(index).txt ./prediction$(index).csv
	rm ./prediction$(index).txt

all:
	cd src/libfm; make all

libFM:
	cd src/libfm; make libFM

clean:
	cd src/libfm; make clean

