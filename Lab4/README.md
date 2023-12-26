# Large Language Model: Chinese Reading Comprehension
此次作業要在 Alpaca or LLaMA 模型上運用 Low rank Adaptation (LoRA) 技術做 fine tuning。  
## Environment Construction
#先去clone中文版的LLaMA and Alpaca模型相關scripts  
````
git clone https://github.com/ymcui/Chinese-LLaMA-Alpaca-2  
````
#安裝conda環境  
````
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh  
bash ./Miniconda3-latest-Linux-x86_64.sh  
````
#重開終端機  
````
conda create --name llm python=3.10  
conda activate llm  
cd Chinese-LLaMA-Alpaca-2  
pip install -r requirements.txt
````
## Data Conversion
一開始，先對資料做轉換，老師給的資料有"AI.xlsx", "AI1000.xlsx"，而我用的模型: Chinese-Alpaca-2系列的指令模型，餵進去的資料格式如圖:  

![data_format](https://github.com/Valerie-Yeh/MachineLearning_NYCU/blob/main/Lab4/image/data_format.png)

也就是原本 xlsx 檔裡的文章、問題、選項1、選項2、選項3、選項4這些 columns 都要被 concatenated into "input" in json file，詳細的資料轉換程式碼在 ConvertData.py 中。  
除此之外，我從訓練資料集 (AI.xlsx) 分離出了大小比例為 8:2 的 training and validation dataset。  
## Fine Tuning
在開始之前，先將 scripts/training/run_clm_sft_with_peft.py 中 line 340, 341, 342 行處 tokenizer 檢查部分進行註解。  
### GPU & Model Information
GPU: 12GB, RTX 2080  
Model: 我一路從 Chinese-Alpaca-2-1.3B、Chinese-Alpaca-2-7B 試到 Chinese-Alpaca-2-13B。最後 Chinese-Alpaca-2-13B 的 score 是3個中最高的，所以就用 Chinese-Alpaca-2-13B了。  
### Hyper Parameters Change
#lora rank 告訴模型如何格式化輸出，降低 lora rank 可以減少GPU的佔用。lora alpha 通常設定是 lora rank 的兩倍  
````
lora_rank = 4  
lora_alpha = 8  
````
#因為在 terminal 上看到訓練的 sequence length 大概在1355左右，所以設一個稍微大的 max_seq_length  
````
max_seq_length = 1450  
````
#模型大概500step才會回頭去看evaluation，這樣設定是為了跑快一點  
````
--eval_steps 500  
````
#調成4是為了避免CUDA out of memory
````
--load_in_kbits 4  
````
下圖為 scripts/training/run_sft.sh 的程式碼截圖，以及存放pretrained_model, dataset_dir, output_dir, validation_file的directory tree
![code_snippet_1](https://github.com/Valerie-Yeh/MachineLearning_NYCU/blob/main/Lab4/image/code_snippet_1.png)

![code_snippet_2](https://github.com/Valerie-Yeh/MachineLearning_NYCU/blob/main/Lab4/image/code_snippet_2.png)

![directory1](https://github.com/Valerie-Yeh/MachineLearning_NYCU/blob/main/Lab4/image/base_model_directory.png)

![directory2](https://github.com/Valerie-Yeh/MachineLearning_NYCU/blob/main/Lab4/image/dataset_directory.png)

![directory3](https://github.com/Valerie-Yeh/MachineLearning_NYCU/blob/main/Lab4/image/code_directory.png)
## Training
````
cd Chinese-LLaMA-Alpaca-2/scripts/training  
./run_sft.sh
````
## Merge Model
在testing前，必須要先將原模型(base_model)與訓練出來的LoRA模型(lora_model)合併  
````
python scripts/merge_llama2_with_chinese_lora_low_mem.py --base_model your_base_model_path --lora_model path_to_lora --output_type huggingface --output_dir path_to_output_dir
````
## Testing
````
python generate.py --base_model path_to_output_dir
````
最後，把csv檔上傳到kaggle，最終成績為0.80285。
