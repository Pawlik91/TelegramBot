import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.net.URL;
import java.nio.charset.Charset;
import java.util.LinkedList;
import java.awt.List;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import com.sun.net.httpserver.HttpServer;

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
	
	private static String addVar(String filterName, String filterVal, String url)
	{
		if(filterName == null || filterVal == null || filterName == "" || filterVal == "")
			return url;
		StringBuilder sb = new StringBuilder();
		sb.append(url);
		if(url.charAt(url.length() - 1) != '?')
			sb.append('&');
		sb.append(filterName);
		sb.append('=');
		sb.append(filterVal);
		return sb.toString();
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
		System.out.println(sb.toString());
		return sb.toString();
	}

	private static String appendPageToURL(String url, int page)
	{
		StringBuilder sb = new StringBuilder();
		sb.append(url);
		sb.append("&page=");
		sb.append(page);
		return sb.toString();
	}
	
	public static LinkedList<String> getProducts(String brand, String name, String priceFrom, String priceTo, 
			boolean sale,boolean available, String color) throws IOException, JSONException
	{
		String url = createURL(brand, name, priceFrom, priceTo, sale, available, color);
		LinkedList<String> products = new LinkedList<String>();
		
		JSONObject json = getJSONFromURL(url);
		
		int pages = getPagesCount(json);
		products.addAll(createProductList(json, "products"));
		
		for(int i = 2; i <= pages; i++)
		{
			json = getJSONFromURL(appendPageToURL(url, i));
			products.addAll(createProductList(json, "products"));
		}

		return products;
	}
	
	private static JSONObject getJSONFromURL(String url)
	{
		try {
			return readJsonFromUrl(url);
		}
		catch(Exception e)
		{
			return null;
		}
	}
	
	private static int getPagesCount(JSONObject json) throws JSONException
	{
		String meta = json.get("meta").toString();
		String[] metaSplit = meta.split("\"pages\":");
		return Integer.parseInt(metaSplit[1].split(",")[0]);
	}
	
	private static LinkedList<String> createProductList(JSONObject json, String key) throws JSONException
	{
		LinkedList<String> products = new LinkedList<String>();
		if(json == null)
			return products;
		
		JSONArray arr = json.getJSONArray(key);
		
		for(int i = 0; i < arr.length(); i++)
		{
			products.add(arr.get(i).toString());
		}
		return products;
	}
	
	public static void main(String[] args) throws IOException, JSONException {
		LinkedList<String> products = getProducts("LG", "TV", "", "", false, false, "");
		System.out.println(products.size());
	}
}
