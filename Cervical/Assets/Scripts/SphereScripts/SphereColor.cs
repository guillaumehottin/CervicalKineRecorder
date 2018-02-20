using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SphereColor : MonoBehaviour {

    public float sphereGreenToYellowAngle;
    public float sphereYellowToRedAngle;
    public List<int> acquisitionScore;
    public AcquireMovement acquireMovementScript;

    private Camera mainCamera;
    private GameObject sphere;
    private Rigidbody rb;
    private Vector3 orientation;
    private float yaw;
    private float pitch;
    private float roll;
    private float sphereYaw;
    private int color;
    private Color vert = new UnityEngine.Color(0, 255, 0);
    private Color jaune = new UnityEngine.Color(255, 255, 0);
    private Color rouge = new UnityEngine.Color(255, 0, 0);

    // Use this for initialization
    void Start()
    {
        mainCamera = Camera.main;
        sphere = GameObject.Find("Sphere");
        rb = sphere.GetComponent<Rigidbody>();
        acquisitionScore = new List<int>();
    }

    public void Reset()
    {
        Start();
    }

    // Update is called once per frame
    void Update()
    {
        orientation = mainCamera.transform.eulerAngles;
        yaw = orientation[1];
        pitch = orientation[0] * Mathf.Deg2Rad;
        roll = orientation[2] * Mathf.Deg2Rad;

        if (yaw > 180)
        {
            yaw = yaw - 360;
        }

        yaw = yaw * Mathf.Deg2Rad;

        sphereYaw = Mathf.PI / 2 - Mathf.Acos(rb.transform.position.x / 5);

        color = getSphereColor(yaw, sphereYaw);
        if (color == 0)
        {
            sphere.GetComponent<Renderer>().material.color = vert;
        }
        else if (color == 1)
        {
            sphere.GetComponent<Renderer>().material.color = jaune;
        }
        else
        {
            sphere.GetComponent<Renderer>().material.color = rouge;
        }

        if (acquireMovementScript.start && !acquireMovementScript.pause && !acquireMovementScript.stop)
        {
            acquisitionScore.Add(2 - color);
        }


    }

    int getSphereColor(float cameraYaw, float sphereYaw)
    {
        float distance = Mathf.Abs(cameraYaw - sphereYaw);
        if (distance < sphereGreenToYellowAngle)
        {
            return 0;
        }
        else if (distance < sphereYellowToRedAngle)
        {
            return 1;
        }
        else
        {
            return 2;
        }
    }

    public void Delete()
    {
        Destroy(this);
    }
}
