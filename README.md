# strinvader

A unicode denormalization generator - find text which normalizes to some target string


## Text mode
Generates some alternate encodings of a text string, such that normalization will still match.

```
$ strinvader.py --num 4 --text blocked_text
Bˡᵒⓒⓚⓔ𝐝︴𝓉𝒆𝔁𝕥
ᵇₗₒｃｋｅ𝑑﹍𝓽𝓮𝔵𝖙
ⓑℓℴ𝐜𝐤𝐞𝒅﹎𝔱𝔢𝕩𝗍
ｂⅼⓞ𝑐𝑘𝑒𝒹﹏𝕥𝕖𝖝𝘁
```

## Char mode
Shows alternate encodings of each individual character, all normalizing to the provided char.

```
$ ./strinvader.py -f nfkc --char abcd:
: <- ['︓', '﹕', '：']
a <- ['ª', 'ᵃ', 'ₐ', 'ⓐ', 'ａ', '𝐚', '𝑎', '𝒂', '𝒶', '𝓪', '𝔞', '𝕒', '𝖆', '𝖺', '𝗮', '𝘢', '𝙖', '𝚊']
b <- ['ᵇ', 'ⓑ', 'ｂ', '𝐛', '𝑏', '𝒃', '𝒷', '𝓫', '𝔟', '𝕓', '𝖇', '𝖻', '𝗯', '𝘣', '𝙗', '𝚋']
c <- ['ᶜ', 'ⅽ', 'ⓒ', 'ｃ', '𝐜', '𝑐', '𝒄', '𝒸', '𝓬', '𝔠', '𝕔', '𝖈', '𝖼', '𝗰', '𝘤', '𝙘', '𝚌']
d <- ['ᵈ', 'ⅆ', 'ⅾ', 'ⓓ', 'ｄ', '𝐝', '𝑑', '𝒅', '𝒹', '𝓭', '𝔡', '𝕕', '𝖉', '𝖽', '𝗱', '𝘥', '𝙙', '𝚍']
```


## Normalization Forms

Use `--forms` to provide any combination of `lower,upper,nfc,nfd,nfkc,nfkd`, based on what your target supports.

```
$ ./strinvader.py --forms nfkc -n 2 --text "blocked_text"
ᵇₗₒｃ𝐤ｅ𝑑︴𝓽𝓮𝔵𝖙
ⓑℓℴ𝐜𝑘𝐞𝒅﹍𝔱𝔢𝕩𝗍

$ ./strinvader.py --forms lower -n 2 --text "blocked_text"
BLOCKED_TEXT
BLOCKED_TEXT
```
