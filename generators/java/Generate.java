
import java.io.File;
import java.io.StringWriter;
import java.io.IOException;
import java.nio.file.Files;

import java.util.ArrayList;
import java.util.HashMap;
import java.lang.Long;


// Depends on JSON.simple
// https://github.com/fangyidong/json-simple
// or apt install libjson-simple-java
import org.json.simple.JSONObject;
import org.json.simple.JSONValue;
import org.json.simple.JSONArray;

class Generate {

  interface Normalizer {
    public String normalize(String inp);
  }

  public static String database_name(String subname) {
    try {
      String version = System.getProperty("java.version");
      String major = version.split("\\.", 0)[0];
      String minor = version.split("\\.", 0)[1];

      if (major.equals("1")) {
        return "java" + major + "." + minor + "_" + subname;
      } else {
        return "java" + major + "_" + subname;
      }
    } catch (Exception e) {
      String fallback = "java_" + subname;
      System.out.println("Unable to find a good java version description. Falling back to " + fallback + " as a filename.");
      return fallback;
    }

  }

  public static ArrayList<Long> get_codepoints(File inputfile) throws IOException {
    byte[] bytes = Files.readAllBytes(inputfile.toPath());
    String json_data = new String(bytes);

    JSONArray list = (JSONArray) JSONValue.parse(json_data);

    ArrayList<Long> ret = new ArrayList<Long>();

    for (Object o : list ) {
      Long v = (Long) o;
      ret.add(v);
    }

    return ret;
  }

  static String from_cp(Long codepoint) {
    return new String(new int[] { codepoint.intValue() }, 0, 1);
  }

  static void add(HashMap< String, ArrayList<Long> > dict, String key, Long value) {
    dict.putIfAbsent(key, new ArrayList<Long>());

    ArrayList<Long> l = dict.get(key);
    l.add(value);
  }

  static JSONObject make_list_dict(HashMap< String, ArrayList<Long> > data) {

    JSONObject ret = new JSONObject();
    for (String k : data.keySet()) {
      JSONArray arr = new JSONArray();

      ArrayList<Long> codepoints = data.get(k);
      for (Long cp : codepoints) {
        arr.add(cp);
      }

      ret.put(k, arr);
    }

    return ret;
  }

  static void make_single_database(ArrayList<Long> codepoints, File dest_dir, String db_name, Normalizer norm) {

    File dest_file = new File(dest_dir, database_name(db_name) + ".json");
    if (dest_file.exists()) {
      System.out.println("Output file " + dest_file + " exists. Skipping.");
      return;
    }

    System.out.println("Generating database at " + dest_file);

    HashMap< String, ArrayList<Long> > single = new HashMap< String, ArrayList<Long> >();
    HashMap< String, ArrayList<Long> > multi = new HashMap< String, ArrayList<Long> >();

    for (Long l : codepoints) {
      String inp = from_cp(l);

      String norm_str = norm.normalize(inp);

      if (norm_str.equals("")) continue;
      if (norm_str.contains(inp)) continue;

      if (norm_str.length() == 1) {
        add(single, norm_str, l);

      } else {
        add(multi, norm_str, l);
        //System.out.println(inp + " => " + norm_str);
      }
    }


    JSONObject db = new JSONObject();

    db.put("single", make_list_dict(single));
    db.put("multi", make_list_dict(multi));

    StringWriter out = new StringWriter();

    try {
      JSONValue.writeJSONString(db, out);
    } catch (IOException e) {
      System.out.println("Failed to serialize to JSON: " + e.toString());
      return;
    }

    String json_data = out.toString();


    try {
      Files.write(dest_file.toPath(), json_data.getBytes());
    } catch (IOException e) {
      System.out.println("Failed to write database to disk: " + e.toString());
      return;
    }



  }

  public static void main(String[] args) {

    File cp_file = new File("../codepoints.json");
    if (args.length >= 1) {
      cp_file = new File(args[0]);
    }

    if (!cp_file.exists()) {
      System.out.println("The codepoints file " + cp_file.toString() + " doesn't exist. Provide a JSON list of integers, please!");
      return;
    }

    File dest_dir = new File("../../databases/");
    if (args.length >= 2) {
      dest_dir = new File(args[1]);
    }

    if (!dest_dir.isDirectory()) {
      System.out.println("The destination directory " + dest_dir.toString() + " isn't a directory. Failing.");
      return;
    }



    System.out.println("Using " + cp_file + " as a list of codepoints.");


    ArrayList<Long> codepoints;
    try {
      codepoints = get_codepoints(cp_file);
    } catch (IOException e) {
      System.out.println("Unable to load codepoints from " + cp_file + ".");
      return;
    }

    System.out.println("Loaded " + codepoints.size() + " codepoints.");



    /*
     * Normalization functions. Feel free to add more here.
     */

    make_single_database(codepoints, dest_dir, "lower", new Normalizer() {
      public String normalize(String inp) {
        return inp.toLowerCase();
      }
    });

    make_single_database(codepoints, dest_dir, "upper", new Normalizer() {
      public String normalize(String inp) {
        return inp.toUpperCase();
      }
    });



  }
}
