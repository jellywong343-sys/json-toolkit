# JSON 宸ュ叿绠?
[English](README.md)

涓€涓敤浜庢牸寮忓寲銆佸帇缂┿€佹牎楠屻€佹帓搴忋€佹煡璇㈠拰姣旇緝 JSON 鏂囦欢鐨勫懡浠よ宸ュ叿銆?
## 涓昏鍔熻兘

- 缇庡寲鎴栧帇缂?JSON銆?- 涓€娆℃牎楠屼竴涓垨澶氫釜鏂囦欢銆?- 閫掑綊鎺掑簭瀵硅薄閿悕銆?- 浣跨敤 `items[0].name` 褰㈠紡鐨勮矾寰勬煡璇㈡暟鎹€?- 杈撳嚭缁撴瀯鍖栥€佸甫璺緞鐨勫樊寮傜粨鏋溿€?- 浠呬娇鐢?Python 鏍囧噯搴撱€?
## 瀹夎

```bash
git clone https://github.com/jellywong343-sys/json-toolkit.git
cd json-toolkit
python -m pip install -e .
```

## 浣跨敤

```bash
json-toolkit validate examples/sample.json
json-toolkit format examples/sample.json
json-toolkit minify examples/sample.json -o compact.json
json-toolkit sort examples/sample.json -o sorted.json
json-toolkit query examples/sample.json tags[0]
json-toolkit diff examples/sample.json examples/sample-updated.json
```

`diff` 鍙戠幇宸紓鏃朵細杩斿洖閫€鍑轰唬鐮?1锛岄€傚悎鑷姩鍖栨鏌ャ€?
## 娴嬭瘯

```bash
python -m unittest discover -s tests -v
```

## 寮€婧愬崗璁?
MIT




