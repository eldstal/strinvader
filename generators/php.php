<?php

/*
 * This script requires the php-intl and php-mbstring extensions
 * apt install php-intl php-mbstring
 */

function add(&$db, $key, $val) {
  if (!array_key_exists($key, $db)) {
    $db[$key] = Array();
  }

  if (!in_array($val, $db[$key])) {
    array_push($db[$key], $val);
  }
}

# $norm_func is a string. The function by this name will be invoked.
# Good god, why does anyone subject themselves to PHP?
function make_db($codepoints, $norm_func) {

  $db = Array("single" => Array(), "multi" => Array());

  foreach ($codepoints as $cp) {
    $src_str = IntlChar::chr($cp);

    $norm_str = $norm_func($src_str);

    if ($norm_str === $src_str) continue;

    if (mb_strlen($norm_str) == 1) {
      add($db["single"], $norm_str, $cp);
    } else {
      add($db["multi"], $norm_str, $cp);
    }
  }

  return $db;
}

function dump_db($db, $path) {
  $js = json_encode($db);

  // Hack: If either single or multi is empty, PHP makes it an empty list.
  // It needs to be an empty dict.
  $js = mb_ereg_replace("\[\]", "{}", $js);
  file_put_contents($path, $js);
}

function urlnorm($txt) {
  $norm = parse_url("http://" . $txt, PHP_URL_HOST);
  if (strstr("xn--", $norm) !== false) return $txt;
  if (mb_strlen($norm) == 0) return $txt;
  return $norm;
}

function lowernorm($txt) {
  $norm = mb_strtolower($txt);
  if (mb_strlen($norm) == 0) return $txt;
  return $norm;
}

function uppernorm($txt) {
  $norm = mb_strtoupper($txt);
  if (mb_strlen($norm) == 0) return $txt;
  return $norm;
}


list($script_path) = get_included_files();
$thisdir = dirname($script_path);
$target_dir = $thisdir . "/../databases";

echo "Target directory: " . $target_dir . "\n";

// Get the list of integer codepoints from our handy dandy JSON array
$codepoints = json_decode(file_get_contents($thisdir . "/codepoints.json"));

$urldb = make_db($codepoints, "urlnorm");
$lowerdb = make_db($codepoints, "lowernorm");
$upperdb = make_db($codepoints, "uppernorm");

dump_db($urldb, $target_dir . "/php_parse_url.json");
dump_db($lowerdb, $target_dir . "/php_lower.json");
dump_db($upperdb, $target_dir . "/php_upper.json");

?>
