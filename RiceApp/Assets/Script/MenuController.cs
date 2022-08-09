using System.Collections;
using System.Collections.Generic;
using System.Threading.Tasks;
using UnityEngine;
using UnityEngine.UI;

public class MenuController : MonoBehaviour
{
    [SerializeField] GameObject snapButton;
    [SerializeField] GameObject chooseImgButton;
    [SerializeField] GameObject statusDisplay;
    [SerializeField] GameObject displayer;
    //[SerializeField] GameObject rawImageObj;

    // Take image option section
    string currentImgPath = "";

    void Start()
    {
        snapButton.GetComponent<Button>().onClick.AddListener(TakePictureOnClick);
        chooseImgButton.GetComponent<Button>().onClick.AddListener(SelectPictureOnClick);
    }
    void Update()
    {
        if (NativeCamera.IsCameraBusy())
        {
            return;
        }
    }
    void TakePictureOnClick()
    {
        TakePicture(SystemInfo.maxTextureSize);
    }      
    void SelectPictureOnClick()
    {
        SelectPicture(SystemInfo.maxTextureSize);
    }    
    private void TakePicture(int maxSize)
    {
        NativeCamera.Permission permission = NativeCamera.TakePicture((path) =>
        {
            if (path != null)
            {
                // Create a Texture2D from the captured image
                //globalTexture = NativeGallery.LoadImageAtPath(path, maxSize, false);
                ResultHolder.globalTexture = NativeGallery.LoadImageAtPath(path, maxSize, false);
                if (ResultHolder.globalTexture == null)
                {
                    Debug.Log("Couldn't load texture from " + path);
                    return;
                }
                else
                {
                    NativeGallery.SaveImageToGallery(ResultHolder.globalTexture, "RiceApp", "rice.jpg");
                    StartCoroutine(APIHandler.APICall_Get(path, ActivateGetDisplay));
                }
            }
        }, maxSize);
    }
    private void SelectPicture(int maxSize)
    {
        NativeGallery.Permission permission = NativeGallery.GetImageFromGallery((path) =>
        {
            if (path != null)
            {
                //globalTexture = NativeGallery.LoadImageAtPath(path, maxSize, false);
                ResultHolder.globalTexture = NativeGallery.LoadImageAtPath(path, maxSize, false);
                if (ResultHolder.globalTexture == null)
                {
                    Debug.Log("Couldn't load texture from " + path);
                    return;
                }
                else
                {
                    StartCoroutine(APIHandler.APICall_Get(path, ActivateGetDisplay));
                }
            }
        });
    }    
    private void ActivateGetDisplay()
    {
        Instantiate(displayer, transform.position, Quaternion.identity);
        //displayer.SetActive(true);
        //rawImageObj.GetComponent<RawImage>().texture = globalTexture;
    }     
}