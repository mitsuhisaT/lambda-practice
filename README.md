# lambda-practice
Practice AWS Lambda using Python

## practice

### execute-ffmpeg


Layer 設定
ffmpeg-bin, ffmpeg-python と一緒に ZIP すると、

```text
1 validation error detected: Value '[]' at 'layers' failed to satisfy constraint: Member must satisfy constraint: [Member must have length less than or equal to 140, Member must have length greater than or equal to 1, Member must satisfy regular expression pattern: (arn:[a-zA-Z0-9-]+:lambda:[a-zA-Z0-9-]+:\d{12}:layer:[a-zA-Z0-9-_]+:[0-9]+)|(arn:[a-zA-Z0-9-]+:lambda:::awslayer:[a-zA-Z0-9-_]+)]
```

ffmpeg-bin と ffmpeg-python を分けて ZIP して Layer 登録すれば、Layer 設定＆実行も問題ない。
