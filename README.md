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
a <- ['ａ', '𝒂', 'ᵃ', '𝘢', '𝖆', 'ª', '𝓪', '𝚊', '𝑎', '𝗮', 'ₐ', 'ⓐ', '𝕒', '𝖺', '𝒶', '𝙖', '𝐚', '𝔞']
b <- ['ｂ', '𝒃', '𝘣', '𝙗', 'ᵇ', '𝖇', '𝓫', '𝚋', '𝑏', '𝗯', 'ⓑ', '𝕓', '𝖻', '𝒷', '𝐛', '𝔟']
c <- ['𝔠', 'ｃ', '𝒄', '𝘤', '𝖈', '𝙘', '𝓬', '𝐜', '𝚌', '𝑐', '𝗰', 'ⓒ', '𝕔', '𝒸', '𝖼', 'ᶜ', 'ⅽ']
d <- ['𝔡', 'ｄ', '𝒅', 'ⅆ', '𝘥', 'ᵈ', '𝖉', '𝓭', '𝚍', '𝙙', '𝑑', '𝗱', 'ⓓ', '𝕕', '𝒹', '𝐝', 'ⅾ', '𝖽']
: <- ['：', '︓', '﹕']
cd <- ['㏅']
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
G <- ['𝒢', '𝙂', '𝐆', 'Ｇ', '𝖦', 'g', '𝔊', '𝑮', '𝘎', '𝗚', '𝕲', 'ᴳ', '𝓖', '𝙶', '🄶', '𝐺', 'Ⓖ', '𝔾']
r <- ['𝒓', '𝖗', '𝚛', 'ℛ', 'ℜ', 'ℝ', '𝐫', '𝔯', 'ʳ', '𝘳', 'ᴿ', '𝓇', 'Ⓡ', '𝗋', 'R', 'ｒ', '𝑟', 'ⓡ', 'ᵣ', '𝕣', '𝙧', '𝓻', '𝗿']
a <- ['𝒂', '𝖆', '𝚊', 'ₐ', '𝐚', '𝔞', '𝘢', 'ª', 'ᴬ', '𝒶', 'Ⓐ', '𝖺', 'A', 'ａ', 'ᵃ', '𝑎', 'ⓐ', '𝕒', '𝙖', '𝓪', '𝗮']
f <- ['𝒇', '𝖋', '𝚏', '𝐟', 'ᶠ', '𝔣', '𝘧', 'ℱ', 'Ⓕ', '𝒻', '𝖿', 'ｆ', 'F', '𝑓', 'ⓕ', '𝕗', '𝙛', '𝓯', '𝗳']
i <- ['𝒊', '𝖎', 'ℐ', 'ℑ', '𝚒', '𝐢', '𝔦', '𝘪', 'İ', 'ᴵ', 'ℹ', '𝒾', 'Ⓘ', '𝗂', 'ⅈ', 'I', 'ｉ', '𝑖', 'ⓘ', '𝕚', '𝙞', 'Ⅰ', 'ᵢ', 'ⅰ', 'ⁱ', '𝓲', '𝗶']
t <- ['𝘁', '𝒕', '𝖙', 'ₜ', '𝚝', '𝐭', '𝔱', '𝘵', 'ᵀ', '𝓉', 'Ⓣ', '𝗍', 'T', 'ｔ', 'ᵗ', '𝑡', 'ⓣ', '𝕥', '𝙩', '𝓽']
ff <- ['ﬀ']
fi <- ['ﬁ']
ffi <- ['ﬃ']

```


## Normalization Forms

Use `--list` to list the supported normalization forms

Use `--forms` to provide any combination of forms, based on what your target supports.

```
$ ./strinvader.py --forms nfkc --num 2 --text "blocked_text"
ᵇₗₒｃ𝐤ｅ𝑑︴𝓽𝓮𝔵𝖙
ⓑℓℴ𝐜𝑘𝐞𝒅﹍𝔱𝔢𝕩𝗍

$ ./strinvader.py --forms lower upper --num 2 --text "blocked_text"
BLOCKED_TEXT
BLOCKED_TEXT
```

Some normalization forms are application specific. For example, the `URL()` constructor in NodeJS normalizes some unicode text in the hostname:

```
$ ./strinvader.py --forms nodejs_hostname --char www.attacker1337.com
w <- ['ᵂ', 'ⓦ', 'Ⓦ', 'W', 'ʷ']
. <- ['。']
a <- ['A', 'ᵃ', 'ª', 'ᴬ', 'ₐ', 'ⓐ', 'Ⓐ']
t <- ['ᵀ', 'ⓣ', 'Ⓣ', 'T', 'ᵗ', 'ₜ']
c <- ['ℂ', 'C', 'Ⅽ', 'ℭ', 'ⓒ', 'Ⓒ', 'ᶜ', 'ⅽ']
k <- ['Ⓚ', 'K', 'K', 'ᵏ', 'ₖ', 'ᴷ', 'ⓚ']
e <- ['E', 'ⅇ', 'ᵉ', 'ℯ', 'ℰ', 'ᴱ', 'ₑ', 'ⓔ', 'Ⓔ']
r <- ['ⓡ', 'ᵣ', 'Ⓡ', 'R', 'ʳ', 'ℛ', 'ℜ', 'ℝ', 'ᴿ']
1 <- ['1']
3 <- ['3']
7 <- ['7']
o <- ['Ⓞ', 'O', 'ₒ', 'ᵒ', 'ℴ', 'º', 'ᴼ', 'ⓞ']
m <- ['Ⓜ', 'M', 'Ⅿ', 'ᵐ', 'ℳ', 'ₘ', 'ᴹ', 'ⓜ', 'ⅿ']
```
This indicates that `www.ⒶᵀTªⒸKⅇℜ1337.ⒸⓄⓂ` will be parsed by NodeJS's `URL()` as `www.attacker1337.com`



## Differences between normalization forms

To inspect how different forms differ, use the `--diff` flag.

Be aware that most databases don't contain *all* codepoints, only the ones that are affected by that normalization. For example, the `lower` normalization form doesn't contain the lowercase `e`, since `lower("e") == "e"`.

This means that comparing a function like `lower` to a full normalization form such as `nfkc` will yield a *lot* of output.


```
user@HOST:strinvader$ ./strinvader.py --forms lower py_lower --diff
╒═════════════╤═══════════╤═══════════════╕
│ Codepoint   │ lower     │ py_lower      │
╞═════════════╪═══════════╪═══════════════╡
│ İ    0130   │ i    0069 │ i̇   0069+0307 │
╘═════════════╧═══════════╧═══════════════╛
A total of 1/1304 codepoints differ.
```


## Databases

Each database represents one normalization function. For example, the unicode `NFKC` normalization form is represented in the `nfkc` database.
Other databases may represent language-specific normalization functions, for example `py_lower` which represents python's builtin `tolower()` function.

A collection of scripts is included under `generators/`, each generating one or more databases.

If you want to add support for some other target (say, a specific web application which does unicode transformation), this is where it goes! Write a script which can generate a database for your target.

A database is a JSON file with the following format:

```json

{
  "single" : {
    "a" : [ 1234, 5678, 1111 ],
    "b" : [ 1337 ],
    ...
  },

  "multi" : {
    "fqt" : [ 1122, 1442 ],
    "\u00ed\u1ee3" : [ 1523 ],
    ...
  }
}
```

All strings are unicode strings. in `single`, keys are single characters. in `multi`, keys are multi-character strings.

Each number is a decimal representation of a single unicode codepoint. For example, 64259 is the representation of U+FB03 (ﬃ)

## TODO
 * More platform-specific normalizations such as [this](https://twitter.com/0xInfection/status/1383820325574438913)
   * nginx?
   * windows functions?
