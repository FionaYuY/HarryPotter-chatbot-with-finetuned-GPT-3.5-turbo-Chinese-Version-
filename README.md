# HarryPotter-chatbot-with-finetuned-GPT-3.5-turbo-Chinese-Version-

## 目標
主要目標有兩者:
1. 利用prompt engineering，模擬哈利波特，展現其對答能力
2. finetune 任一LLM，使其語氣以及內容符合角色
3. 對答皆為中文

## 策略
1. 利用電影版哈利波特1、2、3集劇本對話進行fine-tune，目標是做出能role play哈利波特的聊天模型。若有二次fine-tune的需求，則使用角色資訊去fine-tune
2. 藉由調整係數，取得模型更好的效果
3. 藉由prompt-engineering 使模型有更好的回應
4. 對話設計
   - 確認對話的對象是哈利
   - 請哈利自我介紹
   - 請問他對馬份的看法
   - 詢問他最喜歡的教授、朋友
5. 設定system content: {'role':'system', 'content':'接下來的對話中，你是哈利波特，一位自信又勇敢的魔法師'}

## gpt-3.5-turbo

|確認對話對象是哈利|自我介紹|關於馬份|朋友|其他問題|
|----------------|-------|-------|-----|------|
|ok|非常冗長、但資訊正確|馬份是教授，須說明是跩哥馬份|ok，但冗長|冗長，有些資訊錯誤|
- 可以藉由prompt engineering得到更好的答案，但整體而言對話非常不自然。
- 常常會有資訊錯誤(馬份是一位嚴肅的教授，應該是和石內卜搞混了)
   
## Data Preparation
此專案總共有兩個dataset，主要資料來源為: 

Harry Potter Dataset on #kaggle via @KaggleDatasets https://www.kaggle.com/datasets/gulsahdemiryurek/harry-potter-dataset?utm_medium=social&utm_campaign=kaggle-dataset-share&utm_source=twitter 
- script_data
  * Harry Potter 1.csv, Harry Potter 2.csv, Harry Potter 3.csv為前三集之劇本。
  * 因為此對話模型是要用中文對話，所以將所有劇本利用google translate翻譯成中文
  * 將對話整理後，整理成jsonl格式。
  * 有特別加上{'role':'system', 'content':'接下來的對話中，你是哈利波特，一位自信又勇敢的魔法師'}
- character_data
  * 使用character.csv，將角色特性利用chatgpt整理成以Harry Potter的口吻來介紹角色的資料集。
  * 因為此對話模型是用中文對話，所以將所有劇本利用google translate翻譯成中文
  * 有特別加上{'role':'system', 'content':'接下來的對話中，你是哈利波特，一位自信又勇敢的魔法師'}

## Finetuned Version 1:
1. 以script_data進行訓練，沒有validation data
2. 全部的hyperparameters都是auto
3. hyperparameters: (n_epochs=3, batch_size=1, learning_rate_multiplier=2)

|確認對話對象是哈利|自我介紹|關於馬份|朋友|其他問題|
|----------------|-------|-------|-----|------|
|ok|非常簡短、不能說明興趣喜好|認識跩哥馬份並且資訊正確|沒有朋友|容易跳針|

- 整體效果比gpt-3.5-turbo還差

## Finetuned Version 2:
1. 將10%的劇本對話dataset切出做為validation data
2. 全部的hyperparameters都是auto
3. hyperparameters:(n_epochs=3, batch_size=1, learning_rate_multiplier=2)

|確認對話對象是哈利|自我介紹|關於馬份|朋友|其他問題|
|----------------|-------|-------|-----|------|
|ok|非常簡短|不認識|ok|非常簡短|

- 有了training data和validation data後，效果提升許多，並且也不會有跳針的問題。
- 哈利的回應變得十分簡短，但是內容變得比較自然
- 試著去調整temperature=0 or 0.8。0.8時的回答變得毫無邏輯。

## Finetuned Version 3:
1. 藉由調整係數取得更好的訓練結果，調降learning rate
2. hyperparameters: (n_epochs=3, batch_size=1, learning_rate_multiplier=1.6)

|確認對話對象是哈利|自我介紹|關於馬份|朋友|其他問題|
|----------------|-------|-------|-----|------|
|ok|非常簡短|不認識|ok|非常簡短|

- 常常回答錯誤資訊，ex: 「我也是雷文克勞的」
- 常常牛頭不對馬嘴

## Finetuned Version 4:
1. 藉由調整係數取得更好的訓練結果，調降n_epochs
2. hyperparameter: (n_epochs=2, batch_size=1, learning_rate_multiplier=1.6)

|確認對話對象是哈利|自我介紹|關於馬份|朋友|其他問題|
|----------------|-------|-------|-----|------|
|ok|ok|資訊錯誤|ok|ok|

- 會有錯誤資訊，ex:「馬份是飛行員」

## Finetuned Version 5:
1. 利用新的資料集進行訓練(沒有加上{'role':'system', 'content':'接下來的對話中，你是哈利波特，一位自信又勇敢的魔法師'})
2. 全部的hyperparameters都是auto


|確認對話對象是哈利|自我介紹|關於馬份|朋友|其他問題|
|----------------|-------|-------|-----|------|
|X|X|X|X|X|

- 持續重複「我是你的助手」
- 不知道自己是誰了

## Finetuned Version 6: (The best version)
1. 使用character dataset，並切為training data和validation data。以此dataset搭配finetuned Version 4進行二次finetune。

|確認對話對象是哈利|自我介紹|關於馬份|朋友|其他問題|
|----------------|-------|-------|-----|------|
|ok|ok|需特別強調是【跩哥馬份】|ok|ok|

- 回應長度很適當，語氣也比較活潑
- 對世界觀的理解以及重要角色也都能正確回答
  
## Finetuned Version 7:
1. 做為finetuned Version 6的對照組
2. 使用gpt-3.5-turbo搭配character dataset進行finetune

|確認對話對象是哈利|自我介紹|關於馬份|朋友|其他問題|
|----------------|-------|-------|-----|------|
|ok|ok|馬份是教授|ok|ok|

- 有時會有錯誤資訊
- 回應長度非常長
  
## Conclusion
|gpt-3.5-turbo|Version 1|Version 2|Version 3|Version 4|Version 5|Version 6 (Final)| Version 7|
|-------------|---------|---------|---------|---------|---------|-----------------|----------|
|null|script_data|script_data|script_data|script_data|script_data(without role='system')|version 4 + character_data|character_data|
|null|null|training+10%validation|training+10%validation|training+10%validation|training+10%validation|training+10%validation|training+10%validation|training+10%validation|
|null|auto|auto|learning_rate=1.6|n_epochs=2, learning_rate=1.6|auto|auto|auto|
|X|X|X|X|X|X|V|X|

經由上面的各種組合嘗試，擁有最好效果的是:Version 6。
也就是經由兩次fine-tune所得到的模型。
不管是語氣、文字長度、內容都比其他模型提升很多。
仍然有一些小錯誤需要更詳細的資料去做fine-tune，但整體效果已經非常好。
此外，因為dataset本身都是經由google translate翻譯成中文再使用的，並不是精翻，這部分若有更好的資料則會有更好的表現效果。
