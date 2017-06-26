#!/usr/bin/env bash

python src/launcher.py \
	--phase=train \
	--data-path=/opt/maoshaojiang/myProject/simple-syntext/syndata_cn/R_train_241_zj.txt \
	--data-base-dir=/opt/maoshaojiang/myProject/simple-syntext/syndata_cn/recognition/ \
	--log-path=./model/log_06_26+241.txt \
	--attn-num-hidden 128 \
	--batch-size 64 \
	--model-dir=./model/model_06_26+241 \
	--initial-learning-rate=1.0 \
	--no-load-model \
	--num-epoch=1000 \
	--gpu-id=0 \
	--use-gru \
	--steps-per-checkpoint=2000 \
    --target-embedding-size=10
