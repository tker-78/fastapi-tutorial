# FastAPI tutorial

[公式のチュートリアル](https://fastapi.tiangolo.com/ja/tutorial/first-steps/)を実装して
基本的な使い方を学ぶ。


## Tips

### 実行方法
```bash
$ pip install uvicorn
$ uvicorn main:app --reload
```


### BaseModel
リクエストボディのデータモデルとして、BaseModelを使う。

### バリデーション
`Query`を用いて、下記の属性を指定する。
- default
- min_length
- max_length
- pattern
- alias
- deprecated
- title
- description