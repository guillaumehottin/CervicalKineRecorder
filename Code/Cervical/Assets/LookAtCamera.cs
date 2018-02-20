using UnityEngine;
using System.Collections;

public class LookAtCamera : MonoBehaviour
{
    public Camera mainCamera;
    private Vector3 orientation;
    private float yaw;
    private float pitch;
    private float roll;

    void Start()
    {
        mainCamera = Camera.main;
        //transform.Rotate( 180,0,0 );
    }

    void Update()
    {
        orientation = mainCamera.transform.eulerAngles;
        yaw = Mathf.Repeat(Mathf.PI/2 - orientation[1] * Mathf.Deg2Rad, 2*Mathf.PI);
        pitch = Mathf.Repeat(orientation[0] * Mathf.Deg2Rad + Mathf.PI/2, Mathf.PI);
        //pitch = orientation[0] * Mathf.Deg2Rad;
        //pitch = pitch + Mathf.PI / 2;
        roll = orientation[2] * Mathf.Deg2Rad;
        
        transform.position = new Vector3(3 * Mathf.Sin(pitch)*Mathf.Cos(yaw), 3 * Mathf.Cos(pitch), 3 * Mathf.Sin(pitch) * Mathf.Sin(yaw));
        transform.rotation = mainCamera.transform.rotation;
    }
}