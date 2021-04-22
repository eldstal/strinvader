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

function hostname_norm(txt) {
  try {
    u = new URL("http://" + txt);
    txt_n = u.hostname;

    // This is supposed to be there.
    // Not interesting to us.
    if (txt_n.includes("xn--")) {
      return txt;
    }

    if ([...txt_n].length == 0) return txt

    return txt_n;
  } catch {
    return txt;
  }
}

function urlpath_norm(txt) {
  try {
    u = new URL("http://example.com/" + txt);
    txt_n = u.pathname;

    txt_n = txt_n.replace(new RegExp("^/"), "")
    txt_n = txt_n.replace(new RegExp("%[0-9A-F][0-9A-F]"), "")

    if ([...txt_n].length == 0) return txt

    return txt_n;
  } catch {
    return txt;
  }
}

norm = make_db(codepoints, txt => { return txt.normalize() });
lower = make_db(codepoints, txt => { return txt.toLowerCase() });
upper = make_db(codepoints, txt => { return txt.toUpperCase() });
hostname = make_db(codepoints, hostname_norm);
//urlpath = make_db(codepoints, urlpath_norm);


dump(target_dir + "/nodejs_normalize.json", norm)
dump(target_dir + "/nodejs_lower.json", lower)
dump(target_dir + "/nodejs_upper.json", upper)
dump(target_dir + "/nodejs_hostname.json", hostname)
//dump(target_dir + "/nodejs_urlpath.json", urlpath)
