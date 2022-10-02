using System.Collections;
using System.Collections.Generic;
using System.Threading.Tasks;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class MenuController : MonoBehaviour
{
    [SerializeField] GameObject snapButton;
    [SerializeField] GameObject chooseImgButton;
    [SerializeField] GameObject statusDisplay;
    [SerializeField] GameObject displayer;
    [SerializeField] GameObject loader;
    [SerializeField] GameObject errorNoti;
    [SerializeField] TMP_Text errorText;
    [SerializeField] Button errConfirm;

    private int timeElapsed = 0;
    private bool awaitProcessing = false;
    

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
        if (timeElapsed > 10)
        {
            ProcErr();
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
                    awaitProcessing = true;
                    StartCoroutine(APIHandler.APICall_Get(path, () =>
                    {
                        ActivateGetDisplay();
                        loader.SetActive(false);
                        awaitProcessing = false;
                    }, ProcErr));
                    loader.SetActive(true);
                    StartTimer();
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
                    awaitProcessing = true;
                    StartCoroutine(APIHandler.APICall_Get(path, async () =>
                    {
                        ActivateGetDisplay();
                        loader.SetActive(false);
                        awaitProcessing = false;
                    }, ProcErr));
                    loader.SetActive(true);
                    StartTimer();
                    //StartCoroutine(APIHandler.APICall_Save(path, 1, () => Debug.Log("Success"), () => Debug.Log("failed to sent image to server")));
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
    private async void StartTimer()
    {
        while (true)
        {
            if (awaitProcessing == false) return;
            await Task.Delay(1000);
            timeElapsed++;
        }    
    }  
    private void ProcErr()
    {
        loader.SetActive(false);
        ResultHolder.RefreshResult(new ReturnedClass(404));
        ActivateErrorDisplay();
        timeElapsed = 0;
        awaitProcessing = false;
    }    

    public void ActivateErrorDisplay()
    {
        string _error = "";
        switch (ResultHolder.result.errorStat)
        {
            case 0:
                _error = "Your image was taken in a too low-light condition";
                break;
            case -1:
                _error = "Your image was taken in a too bright condition";
                break;
            case -2:
                _error = "Your image is too blurry";
                break;
            case -3:
                _error = "Your image is too blurry and taken in a low-light condition";
                break;
            case -4:
                _error = "Your image is too blurry and taken in a too bright condition";
                break;
            default:
                _error = "Something wrong happen and we can't process your image. Please try again later.";
                break;
        }
        errorText.text = $"Reason: {_error}";
        errConfirm.onClick.AddListener(() => errorNoti.SetActive(false));
        errorNoti.SetActive(true);
    }    
}