using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.IO;

public class ToggleButton : MonoBehaviour
{
    public GameObject toggle;
    float y_change = (float)7;
    public string name;

    bool ispressed = false; //true - pressed

    void TaskOnClick()
    {
        Debug.Log("You have clicked the button!");
        if (!ispressed)
        {
            toggle.transform.Translate(0, y_change, 0);
            Manager1.myWriter.WriteLine("c&" +name + ":0");
            ispressed = true;
        }
        else {
            toggle.transform.Translate(0, -y_change, 0);
            Manager1.myWriter.WriteLine("c&" + name + ":1");
            ispressed = false;
        }

    }

    // Update is called once per frame
    void Update()
    {

    }
}

