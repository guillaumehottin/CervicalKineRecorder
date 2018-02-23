using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// Script that controls the two lines on the floor to show the limit of the ball movement
/// </summary>
public class LimitsControl : MonoBehaviour
{
    public float sphereLimitAngle; // The limit angle of the sphere in degrees
    
    private GameObject leftLimit;
    private GameObject rightLimit;

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
        leftLimit = GameObject.Find("LeftLimit");
        rightLimit = GameObject.Find("RightLimit");
        leftLimit.transform.eulerAngles = new Vector3(0, -sphereLimitAngle, 0);
        rightLimit.transform.eulerAngles = new Vector3(0, sphereLimitAngle, 0);
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
