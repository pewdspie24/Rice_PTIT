using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
public class DisplayerController : MonoBehaviour
{
    public static int displayMode = 0;              // 0 - loaded from image taken, 1 - loaded from image chosen from gallery
    GameObject mainMenuObj;
    [SerializeField] GameObject thisObj;
    [SerializeField] GameObject imageContainer;
    [SerializeField] GameObject predictYes;
    [SerializeField] GameObject predictNo;
    [SerializeField] GameObject displayedText;
    [SerializeField] GameObject dropdown;
    [SerializeField] GameObject saveImgToServer;
    // Start is called before the first frame update
    void Start()
    {
        mainMenuObj = GameObject.FindGameObjectWithTag("MainMenu");
        if (ResultHolder.result.errorStat != 1)
        {
            mainMenuObj.GetComponent<MenuController>().ActivateErrorDisplay();
            Destroy(this.gameObject);
        }
        else
        { 
            mainMenuObj.SetActive(false);
            thisObj.transform.position = new Vector3(thisObj.transform.position.x, thisObj.transform.position.y, thisObj.transform.position.z + 10);
            imageContainer.GetComponent<RawImage>().texture = ResultHolder.globalTexture;
            //Debug.Log($"class:{ResultHolder.result.type},conf:{ResultHolder.result.confidence}");
            DisplayResult();
        }
    }
    void DisplayResult()
    {
        
        predictNo.SetActive(true);
        predictYes.SetActive(true);
        predictYes.GetComponent<Button>().onClick.AddListener(Exit);
        predictNo.GetComponent<Button>().onClick.AddListener(InitSavingImgFunctionallity);
        displayedText.GetComponent<Text>().text = $"Model's prediction: {ResultHolder.result.type}\nConfidence score: {ResultHolder.result.confidence}\n\nAre the prediction correct?";
    }
    void DisplayUserPrompt()
    {
        predictNo.SetActive(false);
        predictYes.SetActive(false);
        displayedText.GetComponent<Text>().text = $"Please choose the correct state for the image chosen above";
        InitSavingImgFunctionallity();
    }    
    void InitSavingImgFunctionallity()
    {
        dropdown.SetActive(true);
        saveImgToServer.SetActive(true);
        saveImgToServer.GetComponent<Button>().onClick.AddListener(SaveImgButtonFunctionallity);
    }    
    void SaveImgButtonFunctionallity()
    {
        int _class = dropdown.GetComponent<TMP_Dropdown>().value + 1;
        Texture2D tex = (Texture2D)imageContainer.GetComponent<RawImage>().texture;
        byte[] pngFile = tex.EncodeToJPG(100);
        StartCoroutine(APIHandler.APICall_Save(pngFile, _class,() => Exit(), () => Debug.Log("failed to sent image to server")));
    }    
    void Exit()
    {
        Texture2D tex = (Texture2D)imageContainer.GetComponent<RawImage>().texture;
        byte[] pngFile = tex.EncodeToJPG(100);
        StartCoroutine(APIHandler.APICall_Save(pngFile, APIHandler.globalSave._intClass, () => Exit(), () => Debug.Log("failed to sent image to server")));
        mainMenuObj.SetActive(true);
        dropdown.SetActive(false);
        saveImgToServer.SetActive(false);
        thisObj.SetActive(false);
        Destroy(thisObj);
    }    
}
