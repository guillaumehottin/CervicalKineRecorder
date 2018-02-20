using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class LimitsControl : MonoBehaviour
{
    public float sphereLimitAngle;

    private float angle;
    private GameObject leftLimit;
    private GameObject rightLimit;
    private float waitedTime;
    private bool waitingLimit;
    private bool waitingCountdown;
    private int tripsDone;
    private bool stop;

    // Use this for initialization
    void Start()
    {
        leftLimit = GameObject.Find("LeftLimit");
        rightLimit = GameObject.Find("RightLimit");
        leftLimit.transform.eulerAngles = new Vector3(0, -sphereLimitAngle, 0);

        rightLimit.transform.eulerAngles = new Vector3(0, sphereLimitAngle, 0);
    }

    // Update is called once per frame
    void Update()
    {
    }


    public void Reset()
    {
        Start();
    }

    public void Delete()
    {
        Destroy(this);
    }
}
