using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System;

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
        outputFilePath = ".orpl";
        mainCamera = Camera.main;
        start = false;
        stop = false;
        pause = true;
        write = true;
        timeFromLastAcquisition = 0;
        timeBetweenAcquisition = 1 / (float)acquisitionFrequency;
        numberOfFrames = 0;
        acquisitionsList = new List<String>();

        if (!Directory.Exists("tests"))
        {
            Directory.CreateDirectory("tests");
        }

        if (!Directory.Exists("tests/" + profileName))
        {
            Directory.CreateDirectory("tests/" + profileName);
        }

        outputFilePath = "tests/" + profileName + "/" + System.DateTime.Now.ToString("yyyy_MM_dd_HH_mm_ss") + "_" + outputFilePath;
        sr = File.CreateText(outputFilePath);
        sr.WriteLine("yaw pitch roll");
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
            numberOfFrames++;
            timeFromLastAcquisition += Time.deltaTime;
            if (timeFromLastAcquisition > timeBetweenAcquisition)
            {
                orientation = mainCamera.transform.eulerAngles;
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

                //sr = File.AppendText(outputFilePath);
                //sr.WriteLine("{0} {1} {2}", yaw, pitch, roll);
                //sr.Close();
                timeFromLastAcquisition = 0;
            }
        }
        else if (stop && write)
        {
            sr = File.AppendText(outputFilePath);
            foreach (string acquisition in acquisitionsList)
            {
                sr.WriteLine(acquisition);
            }
            sr.Close();
            write = false;
        }
    }

    public void Delete()
    {
        Destroy(this);
    }
}
