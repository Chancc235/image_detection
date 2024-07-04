# Blur and Bright Detection


```
pip install -U -r requirements.txt
```

```bash
# save this information to json
python main.py -i input_directory/ -s results.json

# -t 模糊度阈值，小于阈值为模糊，默认为2
# -b 亮度阈值，小于阈值为明亮，默认为1
