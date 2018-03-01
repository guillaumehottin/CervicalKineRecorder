using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System;

/// <summary>
/// This class allows to get the rotation of the headset following the 3 euler angles (yaw, pitch roll)
/// It does this the closest possible to acquistionFrequency times per second
/// It then outputs it in the file tmp.orpl
/// </summary>
public class AcquireMovement : MonoBehaviour {

    public string outputFilePath;
    public string profileName;
    public bool start;
    public bool stop;
    public bool pause;
    public int acquisitionFrequency;
    public int numberOfFrames;

    private StreamWriter sr;
    private Camera mainCamera;
    private Vector3 orientation;
    private float yaw;
    private float pitch;
    private float roll;
    private float timeBetweenAcquisition;
    private float timeFromLastAcquisition;
    private List<string> acquisitionsList;
    private bool write;
    // Use this for initialization
    void Start () {
        outputFilePath = "tmp.orpl";
        mainCamera = Camera.main;
        start = false; // set to true when the sphere hits the left border for the first time
        stop = false; // set to true when the sphere hits the left border after the right number of trips
        pause = true;
        write = true; // set to true after the acquisition is finished, then false when all the list has been written to a file
        timeFromLastAcquisition = 0; // the time from the last acquired position
        timeBetweenAcquisition = 1 / (float)acquisitionFrequency; // the minimum time between two acquisitions
        numberOfFrames = 0;
        acquisitionsList = new List<String>(); // the list to store all the positions

        if (!Directory.Exists("tests"))
        {
            Directory.CreateDirectory("tests");
        }

        if (!Directory.Exists("tests/" + profileName))
        {
            Directory.CreateDirectory("tests/" + profileName);
        }
        
        sr = File.CreateText(outputFilePath);
        sr.WriteLine("yaw pitch roll"); // header of the output file
        sr.Close();
    }

    public void Reset()
    {
        Start();
    }
	
	// Update is called once per frame
	void Update () {
        if (start && !stop && !pause)
        {
            timeFromLastAcquisition += Time.deltaTime; // add the time from the last frame
            if (timeFromLastAcquisition > timeBetweenAcquisition) // do an acquisition if the time is correct
            {
                orientation = mainCamera.transform.eulerAngles; // gets the 3 angles in degrees in an array of size 3
                yaw = orientation[1];
                pitch = orientation[0];
                roll = orientation[2];

                if (yaw > 180)
                {
                    yaw = yaw - 360;
                }

                if (pitch > 180)
                {
                    pitch = pitch - 360;
                }

                if (roll > 180)
                {
                    roll = roll - 360;
                }

                acquisitionsList.Add(yaw + " " + pitch +  " " + roll);
                timeFromLastAcquisition = 0;
            }
        }
        else if (stop && write) // acquisition ended, writing to the file
        {
            sr = File.AppendText(outputFilePath);
            foreach (string acquisition in acquisitionsList)
            {
                sr.WriteLine(acquisition);
            }
            sr.Close();
            write = false; // don't continue writing
        }
    }

    public void Delete()
    {
        Destroy(this);
    }
}
