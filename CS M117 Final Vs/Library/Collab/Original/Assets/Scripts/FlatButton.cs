using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;

public class FlatButton : MonoBehaviour //,IPointerDownHandler, IPointerUpHandler
{
    public GameObject toggle;
    float y_change = 5f;
    public string name;

    public void OnPointerDown()
    {
        toggle.transform.Translate(0, y_change, 0);
    }

    public void OnPointerUp()
    {
        toggle.transform.Translate(0, -y_change, 0);
        Manager1.myWriter.WriteLine("c&" + name + ":1");
        Manager1.grid1GameBoard.updateGameBoard(name, "1");
    }

}