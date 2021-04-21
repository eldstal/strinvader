fs = require('fs')

let dir = __dirname
let target_dir = dir + "/../databases/"

let rawcp = fs.readFileSync(dir + '/codepoints.json')
let codepoints = JSON.parse(rawcp)


function add(dict, key, val) {
  if (!(key in dict)) {
    dict[key] = []
  }

  if (!(val in dict[key])) {
    dict[key].push(val);
  }
}


function make_db(codepoints, normfunc) {

  let db = { "single": {}, "multi": {} }

  for (cp in codepoints) {

    cp = parseInt(cp)
    src_str = String.fromCodePoint(cp);

    //norm_str = src_str.normalize();
    //norm_str = src_str.toLowerCase();
    norm_str = normfunc(src_str)

    if (norm_str == src_str) continue;

    if ([...norm_str].length == 1) {
      add(db["single"], norm_str, cp);
    } else {
      add(db["multi"], norm_str, cp);
    }
  }

  return db

}

function dump(path, db) {
  console.log(path)
  data = JSON.stringify(db);
  fs.writeFileSync(path, data);
}

norm = make_db(codepoints, txt => { return txt.normalize() });
lower = make_db(codepoints, txt => { return txt.toLowerCase() });
upper = make_db(codepoints, txt => { return txt.toUpperCase() });


dump(target_dir + "/nodejs_normalize.json", norm)
dump(target_dir + "/nodejs_lower.json", lower)
dump(target_dir + "/nodejs_upper.json", upper)
