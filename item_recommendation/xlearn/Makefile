stk_dir = ./tmp_stk

hello :
	echo "please input a instruction"

split_data :
	./scripts/split_data.py 5 ./data/combine.tsv.libfm ./data/test.tsv.libfm ./data/parts

accumulate :
	./scripts/accumulator.py $(stk_dir)

stacking :
	./scripts/stacking.py ./data/parts ./tmp_stk ./scripts

xgboost :
	./scripts/xgb.py $(stk_dir)/0

sxlearn :
#   xlearn_train.py k lambda lr early epoch ftrain fvalid ftest fpred
	./scripts/xlearn_train.py 8 1 0.01 True 1000 $(stk_dir)/0/train.libfm $(stk_dir)/0/valid.libfm $(stk_dir)/0/test.libfm $(stk_dir)/0/tprediction.txt

wraper :
	./scripts/prediction_to_format_csv.py ../data/test.tsv $(stk_dir)/0/tprediction.txt $(stk_dir)/0/tprediction.csv
#	./scripts/prediction_to_format_csv.py ../data/test.tsv ./stack_predictions/B0.pred ./stack_predictions/B0.pred.csv
