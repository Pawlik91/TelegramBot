import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.net.URL;
import java.nio.charset.Charset;

import org.json.JSONException;
import org.json.JSONObject;

public class JsonReader {

  private static String readAll(Reader rd) throws IOException {
    StringBuilder sb = new StringBuilder();
    int cp;
    while ((cp = rd.read()) != -1) {
      sb.append((char) cp);
    }
    return sb.toString();
  }

  private static JSONObject readJsonFromUrl(String url) throws IOException, JSONException {
    InputStream is = new URL(url).openStream();
    try {
      BufferedReader rd = new BufferedReader(new InputStreamReader(is, Charset.forName("UTF-8")));
      String jsonText = readAll(rd);
      JSONObject json = new JSONObject(jsonText);
      return json;
    } finally {
      is.close();
    }
  }
  
  private static String createURL(String brand, String name, String priceFrom, String priceTo, 
		  	boolean sale,boolean available, String color)
  {
	  StringBuilder sb = new StringBuilder();
	  sb.append("http://10.1.141.181:3000/products?");
	  boolean set = false;
	  if(brand != null && brand != "") {
		  sb.append("brand=");
		  sb.append(brand);
		  set = true;
	  }
	  if(name != null && name != "")
	  {
		  if(set)
			  sb.append('&');
		  sb.append("name=");
		  sb.append(name);
		  set = true;
	  }
	  if(priceFrom != null && priceFrom != "")
	  {
		  if(set)
			  sb.append('&');
		  sb.append("priceFrom=");
		  sb.append(priceFrom);
		  set = true;
	  }
	  if(priceTo != null && priceTo != "")
	  {
		  if(set)
			  sb.append('&');
		  sb.append("priceTo=");
		  sb.append(priceTo);
		  set = true;
	  }
	  if(sale)
	  {
		  if(set)
			  sb.append('&');
		  sb.append("sale=");
		  sb.append(true);
		  set = true;
	  }
	  if(available)
	  {
		  if(set)
			  sb.append('&');
		  sb.append("available=");
		  sb.append(true);
		  set = true;
	  }
	  if(color != null && color != "")
	  {
		  if(set)
			  sb.append('&');
		  sb.append("color=");
		  sb.append(color);
		  set = true;
	  }
	  System.out.println(sb.toString() + "\n");
	  return sb.toString();
  }
  
  private static String appendPageToURL(String url, int page)
{
	  StringBuilder sb = new StringBuilder();
	  sb.append(url);
	  sb.append("&page=");
	  sb.append(page);
	  System.out.println(sb.toString() + "\n");
	  return sb.toString();
}

  public static String getProducts(String brand, String name, String priceFrom, String priceTo, 
		  	boolean sale,boolean available, String color) throws IOException, JSONException
  {
	  String url = createURL(brand, name, priceFrom, priceTo, sale, available, color);
	  StringBuilder sb = new StringBuilder();
	  JSONObject json;
	  
	  try {
		  json = readJsonFromUrl(url);
	  }
	  catch(Exception e)
	  {
		  return "";
	  }
	  
	  String meta = json.get("meta").toString();
	  String[] metaSplit = meta.split("\"pages\":");
	  int pages = Integer.parseInt(metaSplit[1].split(",")[0]);
	  
	  sb.append(json.get("products").toString());
	  sb.append("\n1\n");
	  for(int i = 2; i < pages; i++)
	  {
		  try {
			  json = readJsonFromUrl(appendPageToURL(url, i));
			  sb.append(json.get("products").toString());
			  sb.append("\n");
			  sb.append(i);
			  sb.append("\n");
		  }
		  catch(Exception e)
		  {
			  sb.toString();
		  }
	  }
	  
	  return sb.toString();
  }
  
  public static void main(String[] args) throws IOException, JSONException {
	  long startTime = System.currentTimeMillis();
	  System.out.println(getProducts("LG", "TV", "", "", false, false, ""));
	  long stopTime = System.currentTimeMillis();
      long elapsedTime = stopTime - startTime;
      System.out.println(elapsedTime / 1e3);
  }
}
