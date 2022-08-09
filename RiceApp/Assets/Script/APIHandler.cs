using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using System.Globalization;

static public class APIHandler
{
    public static int returnedClass = 0;
    public static ReturnedClass globalSave;
    static public IEnumerator APICall_Get(string _imgPath, System.Action callback)
    {
        WWWForm form = new WWWForm();
        string _url = "https://203.162.88.122:18008/getpercent";
        form.AddBinaryData("file", System.IO.File.ReadAllBytes(_imgPath), "riceImg.jpg");
        using (UnityWebRequest www = UnityWebRequest.Post(_url, form))
        {
            www.certificateHandler = new CustomSLLBypass();
            yield return www.SendWebRequest();
            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.Log(www.error);
            }
            else
            {
                string response = System.Text.Encoding.UTF8.GetString(www.downloadHandler.data);
                ResultParser(response);
                Debug.Log("success");
                callback();
            }
        }
    }
    static public IEnumerator APICall_Save(string _path, int _class, System.Action Succeed, System.Action Failed)
    {
        WWWForm form = new WWWForm();
        string _url = "https://203.162.88.122:18008/save";
        form.AddBinaryData("file", System.IO.File.ReadAllBytes(_path));
        form.AddField("class", _class);
        using (UnityWebRequest www = UnityWebRequest.Post(_url, form))
        {
            www.certificateHandler = new CustomSLLBypass();
            yield return www.SendWebRequest();
            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.Log(www.error);
                Failed();
            }
            else
            {
                Succeed();
                Debug.Log("success");
            }
        }
    }static public IEnumerator APICall_Save(byte[] _content, int _class, System.Action Succeed, System.Action Failed)
    {
        WWWForm form = new WWWForm();
        string _url = "https://203.162.88.122:18008/save";
        form.AddBinaryData("file", _content);
        form.AddField("class", _class);
        using (UnityWebRequest www = UnityWebRequest.Post(_url, form))
        {
            www.certificateHandler = new CustomSLLBypass();
            yield return www.SendWebRequest();
            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.Log(www.error);
                Failed();
            }
            else
            {
                Succeed();
                Debug.Log("success");
            }
        }
    }
    static void ResultParser(string result)
    {
        Debug.Log(result);
        result = result.Trim(new char[] { '[', ']', ' ' });
        string[] split = result.Split(',');
        float currentMax = 0.0f;
        int classBelonged = 0;
        int idx = 0;
        foreach (var item in split)
        {
            idx++;
            string _item = item.TrimEnd(',');
            float _c = JsonHandler.ProcessOne(_item);
            if (_c > currentMax)
            {
                classBelonged = idx;
                currentMax = _c;
            }
        }
        SetClass(classBelonged, currentMax);
    }
    static void SetClass(int _idx, float _conf)
    {
        string[] CLASS = new string[] {"UNKNOWN", "BrownSpot", "Healthy", "Hispa", "LeafBlast" };
        globalSave = new ReturnedClass(CLASS[_idx], _conf);
        ResultHolder.RefreshResult(globalSave);
    }
}

internal static class Converter
{
    public static readonly JsonSerializerSettings Settings = new JsonSerializerSettings
    {
        MetadataPropertyHandling = MetadataPropertyHandling.Ignore,
        DateParseHandling = DateParseHandling.None,
        Converters =
            {
                new IsoDateTimeConverter { DateTimeStyles = DateTimeStyles.AssumeUniversal }
            },
    };
}

static public class JsonHandler
{
    public static float ProcessOne(string json)
    {
        json = json.Trim(new char[] { '{', '}', ' ', '"' });
        string[] temp = json.Split(':');
        float converted = 0.0f;
        try
        {
            converted = float.Parse(temp[1]);
        }
        catch (System.Exception)
        {
            Debug.Log($"error converting {temp[0]}, returning min value");
            converted = 0.0f;
            throw;
        }
        return converted;
    }
}
