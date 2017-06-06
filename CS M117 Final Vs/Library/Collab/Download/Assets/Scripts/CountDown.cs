using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class CountDown : MonoBehaviour {

    float timeLeft = 0.0f;
    //public GameObject myslider;
   public static Slider mainSlider;

    public static void TimerReset()
    {
        mainSlider.value = 0.0f;
    }

    // Use this for initialization
    void Start () {
        mainSlider.maxValue = 20;

    }
	
	// Update is called once per frame
	void Update () {
        
        //Debug.Log(timeLeft);
        timeLeft += Time.deltaTime;
        mainSlider.value = timeLeft;
        if (timeLeft > 20.0f )
        {
            GenerateCmd();
            timeLeft = 0.0f;
            mainSlider.value = 0.0f;
            Debug.Log("Timer Ended");
        }
    }

    void GenerateCmd()
    {
        Manager1.commandText.text = Manager1.grid1GameBoard.lateCommand();
    }
}
