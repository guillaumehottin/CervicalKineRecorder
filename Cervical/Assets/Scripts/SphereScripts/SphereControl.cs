using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class SphereControl : MonoBehaviour
{
    public float sphereSpeed;
    public float sphereLimitAngle;
    public float sphereWaitTime;
    public float sphereCountdownTime;
    public int sphereRoundTripNumber;
    public AcquireMovement acquireMovementScript;
    public Text countdownText;
    public Image crossHair;
    public bool start;

    private float angle;
    private Rigidbody rb;
    private float waitedTime;
    private bool waitingLimit;
    private bool waitingCountdown;
    private int tripsDone;
    public bool stop;
    public bool finished;
    private bool firstRoundTripDone = false;

    // Use this for initialization
    void Start()
    {
        rb = GameObject.Find("Sphere").GetComponent<Rigidbody>();
        angle = Mathf.PI / 2;
        waitedTime = 0;
        waitingLimit = false;
        waitingCountdown = true;
        tripsDone = -1;
        stop = false;
        finished = false;
    }

    public void Reset()
    {
        Start();
        //rb = GameObject.Find("Sphere").GetComponent<Rigidbody>();

        //angle = Mathf.PI / 2;
        //waitedTime = 0;
        //waitingLimit = false;
        //waitingCountdown = true;
        //tripsDone = 0;
        //stop = false;
        //finished = false;
    }

    // Update is called once per frame
    void Update()
    {
        if (start)
        {
            if (!waitingLimit && !waitingCountdown && !stop)
            {
                angle += sphereSpeed * Time.deltaTime;
                rb.MovePosition(new Vector3(5 * Mathf.Cos(angle), 0, 5 * Mathf.Sin(angle)));

                if ((angle > (Mathf.PI - sphereLimitAngle) && sphereSpeed > 0) || (angle < sphereLimitAngle && sphereSpeed < 0))
                {
                    //Debug.Log("angle: " + angle + "sphereLimitAngle: " + sphereLimitAngle + "Mathf.PI - sphereLimitAngle: " + (Mathf.PI - sphereLimitAngle));
                    sphereSpeed = -sphereSpeed;
                    waitingLimit = true;
                    acquireMovementScript.pause = true;
                    waitedTime = 0;
                    tripsDone++;
                    stop = tripsDone == 2 * sphereRoundTripNumber;
                    acquireMovementScript.stop = stop;
                }
            }
            else if (waitingLimit && !waitingCountdown && !stop)
            {
                //Debug.Log(angle + " " + limitAngle + " " + (Mathf.PI - limitAngle));
                waitedTime += Time.deltaTime;
                waitingLimit = waitedTime < sphereWaitTime;
                if (!waitingLimit)
                {
                    acquireMovementScript.pause = false;
                }
                if (!firstRoundTripDone)
                {
                    acquireMovementScript.start = true;
                    acquireMovementScript.pause = true;
                    firstRoundTripDone = true;
                }
            }
            else if (waitingCountdown && !stop)
            {
                waitedTime += Time.deltaTime;
                waitingCountdown = waitedTime < sphereCountdownTime;
                if (waitingCountdown)
                {
                    countdownText.text = Mathf.Floor(sphereCountdownTime - waitedTime + 1).ToString();
                }
                else
                {
                    countdownText.text = "";
                    acquireMovementScript.start = true;
                }
            }
            else
            {
                countdownText.text = "FIN";
                acquireMovementScript.stop = true;
                finished = true;
                angle = Mathf.PI / 2;
                rb.MovePosition(new Vector3(5 * Mathf.Cos(angle), 0, 5 * Mathf.Sin(angle)));
            }
        }
    }

    public void Delete()
    {
        Destroy(this);
    }
}
