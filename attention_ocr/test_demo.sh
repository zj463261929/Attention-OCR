#!/usr/bin/env bash

python src/launcher.py \
	--phase=test \
	--data-path=/opt/ligang/data/pic2000_15_data_2017_5_31/WordBBText.txt \
	--data-base-dir=/opt/ligang/data/pic2000_15_data_2017_5_31/result_img_word \
	--log-path=./model/log_06_2_test.txt \
	--attn-num-hidden 512 \
	--batch-size 1 \
	--model-dir=./model/model_06_7 \
	--load-model \
	--num-epoch=1 \
	--gpu-id=1 \
	--output-dir=../results \
	--use-gru \
    --target-embedding-size=20
    
    
    
#/opt/datasets/data/str/mnt/ramdisk/max/90kDICT32px/annotation_test.txt
# /opt/zhangjing/ocr/Attention_OCR/evaluation_data/iiit5k/test.txt
# /dataTwo/zhangjing/ocr/Attention_OCR/evaluation_data/iiit5k
#/opt/ligang/data/pic2000_data_2017_6_15/zj/test_word/test.txt