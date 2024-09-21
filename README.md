# FastAPI tutorial

[公式のチュートリアル](https://fastapi.tiangolo.com/ja/tutorial/first-steps/)を実装して
基本的な使い方を学ぶ。


## Tips

```powershell
[System.Console]::OutputEncoding = [System.Text.Encoding]::GetEncoding("utf-8")
```

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


`Path`を用いて、パスパラメータの属性を指定する。
- le
- ge
- lt
- gt


`Path`の第一引数に`*`を指定することで、
それ以降の引数がキーワード引数化する。

`Body`を用いて、リクエストボディであることを示す。

単一のリクエストボディで、かつ入れ子にしたい場合、
`item: Item = Body(embed=True)`とする。