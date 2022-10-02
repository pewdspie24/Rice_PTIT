using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Post
{
    public string file { get; set; }
}

public class Demo
{
    public string Title { get; set; }
    public string Body { get; set; }
    public int UserId { get; set; }
}
[Serializable]
public class ReturnedClass
{
    public string type { get; set; }
    public int _intClass { get; set; }
    public float confidence { get; set; }
    public int errorStat { get; set; }
    public ReturnedClass()
    {
        type = "UNKNOWN";
        _intClass = 0;
        confidence = 0.0f;
        errorStat = 1;
    }
    public ReturnedClass(int _err)
    {
        type = "UNKNOWN";
        _intClass = 0;
        confidence = 0.0f;
        errorStat = _err;
    }
    public ReturnedClass(string _type, float _confidence)
    {
        type = _type;
        confidence = _confidence;
        switch (type)
        {
            default:
                _intClass = 0;
                break;
            case "BrownSpot":
                _intClass = 1;
                break;
            case "Healthy":
                _intClass = 2;
                break;
            case "Hispa":
                _intClass = 3;
                break;
            case "LeafBlast":
                _intClass = 4;
                break;
        }
        errorStat = 1;
    }
}
[Serializable]
public class Classes
{
    public List<ReturnedClass> classes;

    float _brownConf { get; set; }
    float _healthyConf { get; set; }
    float _hispaConf { get; set; }
    float _blastConf { get; set; }
    //float _brownConf { get { return float.Parse(brownConf); } }
    //float _healthyConf { get { return float.Parse(healthyConf); } }
    //float _hispaConf { get { return float.Parse(hispaConf); } }
    //float _blastConf { get { return float.Parse(blastConf); } }

    public void Init()
    {
        //_brownConf = classes[0].confidence;
        //_healthyConf = classes[1].confidence;
        //_hispaConf = classes[2].confidence;
        //_blastConf = classes[3].confidence;
    }

    public int GetMaximumConf()
    {
        Init();
        float holder = 0.0f;
        int _class = 0;
        if (_brownConf > holder)
        {
            holder = _brownConf;
            _class = 1;
        }
        if (_healthyConf > holder)
        {
            holder = _healthyConf;
            _class = 2;
        }
        if (_hispaConf > holder)
        {
            holder = _hispaConf;
            _class = 3;
        }
        if (_blastConf > holder)
        {
            holder = _blastConf;
            _class = 4;
        }
        return _class;
    }
}
