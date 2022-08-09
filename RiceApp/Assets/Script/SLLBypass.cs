using System.Collections;
using System.Collections.Generic;
using UnityEngine.Networking;

public class CustomSLLBypass : CertificateHandler
{
    protected override bool ValidateCertificate(byte[] certificateData)
    {
        //  WARNING: this method accepts ANY kind of SSL cert
        return true;
    }
}
