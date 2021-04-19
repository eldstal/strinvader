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
$ ./strinvader.py --forms nfkc --char abcd:
: <- ['︓', '﹕', '：']
a <- ['ª', 'ᵃ', 'ₐ', 'ⓐ', 'ａ', '𝐚', '𝑎', '𝒂', '𝒶', '𝓪', '𝔞', '𝕒', '𝖆', '𝖺', '𝗮', '𝘢', '𝙖', '𝚊']
b <- ['ᵇ', 'ⓑ', 'ｂ', '𝐛', '𝑏', '𝒃', '𝒷', '𝓫', '𝔟', '𝕓', '𝖇', '𝖻', '𝗯', '𝘣', '𝙗', '𝚋']
c <- ['ᶜ', 'ⅽ', 'ⓒ', 'ｃ', '𝐜', '𝑐', '𝒄', '𝒸', '𝓬', '𝔠', '𝕔', '𝖈', '𝖼', '𝗰', '𝘤', '𝙘', '𝚌']
d <- ['ᵈ', 'ⅆ', 'ⅾ', 'ⓓ', 'ｄ', '𝐝', '𝑑', '𝒅', '𝒹', '𝓭', '𝔡', '𝕕', '𝖉', '𝖽', '𝗱', '𝘥', '𝙙', '𝚍']
```

## Multi-character replacements
There are single unicode characters which normalize to multiple, such as ligatures (e.g `ﬃ -> ffi`). These are supported and enabled by default.

```
$ ./strinvader.py --num 3 --no-single --text Graffitti
Graﬀitti
Grafﬁtti
Graﬃtti
```

```
$ ./strinvader.py --char Graffitti
G <- ['𝒢', '𝙂', '𝐆', 'Ｇ', '𝖦', '𝔊', '𝑮', '𝘎', '𝗚', '𝕲', 'ᴳ', '𝓖', '𝙶', '🄶', '𝐺', 'Ⓖ', '𝔾']
r <- ['ⓡ', 'ᵣ', '𝕣', '𝓇', '𝙧', '𝐫', '𝗋', '𝗿', '𝔯', 'ｒ', 'ʳ', '𝒓', '𝘳', '𝖗', '𝓻', '𝚛', '𝑟']
f <- ['ᶠ', '𝔣', 'ｆ', '𝒇', '𝘧', '𝖿', '𝖋', '𝓯', '𝚏', '𝑓', '𝗳', 'ⓕ', '𝕗', '𝙛', '𝒻', '𝐟']
i <- ['𝒊', '𝖎', '𝚒', '𝐢', '𝔦', '𝘪', 'ℹ', '𝒾', '𝗂', 'ⅈ', 'ｉ', '𝑖', 'ⓘ', '𝕚', '𝙞', 'ᵢ', 'ⅰ', 'ⁱ', '𝓲', '𝗶']
a <- ['ａ', '𝒂', 'ᵃ', '𝘢', '𝖆', 'ª', '𝓪', '𝚊', '𝑎', '𝗮', 'ₐ', 'ⓐ', '𝕒', '𝖺', '𝒶', '𝙖', '𝐚', '𝔞']
t <- ['𝑡', '𝘁', 'ⓣ', '𝕥', '𝚝', '𝓉', '𝙩', '𝐭', '𝗍', '𝔱', 'ｔ', '𝒕', '𝘵', 'ᵗ', '𝖙', 'ₜ', '𝓽']
ff <- ['ﬀ']
fi <- ['ﬁ']
ffi <- ['ﬃ']
```


## Normalization Forms

Use `--forms` to provide any combination of `lower,upper,nfc,nfd,nfkc,nfkd`, based on what your target supports.

```
$ ./strinvader.py --forms nfkc --num 2 --text "blocked_text"
ᵇₗₒｃ𝐤ｅ𝑑︴𝓽𝓮𝔵𝖙
ⓑℓℴ𝐜𝑘𝐞𝒅﹍𝔱𝔢𝕩𝗍

$ ./strinvader.py --forms lower --num 2 --text "blocked_text"
BLOCKED_TEXT
BLOCKED_TEXT
```


## TODO
 * Platform-specific normalizations such as [this](https://twitter.com/0xInfection/status/1383820325574438913)
   * It would be useful to have a `-f perl` or `-f nodejs` etc, if you know what the target is running.
