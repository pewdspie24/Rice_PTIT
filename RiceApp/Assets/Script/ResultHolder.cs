using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ResultHolder : MonoBehaviour
{
    public static ReturnedClass result = new ReturnedClass();
    public static Texture2D globalTexture;
    // Start is called before the first frame update
    void Start()
    {
        DontDestroyOnLoad(this);
    }
    void Update()
    {
        try
        {
            result = APIHandler.globalSave;
            //Debug.Log($"class:{ResultHolder.result.type},conf:{ResultHolder.result.confidence}");
        }
        catch (System.Exception)
        {
            
        }    
    }
    public static void RefreshResult(ReturnedClass _i)
    {
        result = _i;
    }
}
