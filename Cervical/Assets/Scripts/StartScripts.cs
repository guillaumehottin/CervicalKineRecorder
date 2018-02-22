using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.IO;
using System.Text;
using System.Net.Sockets;
using System;
using System.Linq;

public class StartScripts : MonoBehaviour {

    public float sphereSpeed;
    public float sphereLimitAngle;
    public float sphereWaitTime;
    public float sphereCountdownTime;
    public int sphereRoundTripNumber;
    public float sphereLimitAngleLimits;

    public float sphereGreenToYellowAngle;
    public float sphereYellowToRedAngle;

    public string outputFilePath;
    public int acquisitionFrequency;

    public string profileName;

    private SphereControl sphereControlScript;
    private SphereColor sphereColorScript;
    private AcquireMovement acquireMovementScript;
    private LimitsControl limitsControlScript;
    private s_TCP sTCPScript;
    private SocketClient socketClientScript;
    private SocketReceive socketReceiveJob;

    private string confFile = "cervical.conf";

    public Text countdownText;
    public Image crosshair;

    public bool receivebool = true;
    public int messages = 0;

    private string message;
    private string state;

    private float waitTime = 0.3f;
    private float waitedTime;

    private bool conf = false;
    private bool connected = false;
    private int port = 50007;

    // Use this for initialization
    void Start () {
        if (conf)
        {
            LoadConf();
            
            sphereSpeed = sphereSpeed * Mathf.Deg2Rad;
            sphereLimitAngleLimits = sphereLimitAngle;
            sphereLimitAngle = Mathf.PI / 2 - sphereLimitAngle * Mathf.Deg2Rad;

            countdownText.text = "EN ATTENTE";
            gameObject.AddComponent<SphereControl>();
            sphereControlScript = gameObject.GetComponent<SphereControl>();
            sphereControlScript.sphereSpeed = sphereSpeed;
            sphereControlScript.sphereLimitAngle = sphereLimitAngle;
            sphereControlScript.sphereWaitTime = sphereWaitTime;
            sphereControlScript.sphereCountdownTime = sphereCountdownTime;
            sphereControlScript.countdownText = countdownText;
            sphereControlScript.sphereRoundTripNumber = sphereRoundTripNumber;

            gameObject.AddComponent<SphereColor>();
            sphereColorScript = gameObject.GetComponent<SphereColor>();
            sphereColorScript.sphereGreenToYellowAngle = sphereGreenToYellowAngle;
            sphereColorScript.sphereYellowToRedAngle = sphereYellowToRedAngle;

            gameObject.AddComponent<AcquireMovement>();
            acquireMovementScript = gameObject.GetComponent<AcquireMovement>();
            acquireMovementScript.outputFilePath = outputFilePath;
            acquireMovementScript.acquisitionFrequency = acquisitionFrequency;
            acquireMovementScript.profileName = profileName;

            sphereControlScript.acquireMovementScript = acquireMovementScript;

            gameObject.AddComponent<LimitsControl>();
            limitsControlScript = gameObject.GetComponent<LimitsControl>();
            limitsControlScript.sphereLimitAngle = sphereLimitAngleLimits;


            sphereControlScript.start = true;
        }
        else
        {
            state = "connect";
        }


        
        
    }

    // Update is called once per frame
    void Update() {
        if (!conf)
        {
            if (state.Equals("wait"))
            {
                waitedTime += Time.deltaTime;
                if (waitedTime > waitTime)
                {
                    state = "connect";
                }
            }
            else if (state.Equals("connect"))
            {
                connected = SocketClient.connectSocket("127.0.0.1", port);
                if (connected)
                {
                    Debug.Log("connected new");
                    Debug.Log(port);
                    port++;
                    state = "receive";
                }

            }
            else if (state.Equals("receive"))
            {
                socketReceiveJob = new SocketReceive();
                socketReceiveJob.Start();

                state = "checkReceive";
            }
            else if (state.Equals("checkReceive"))
            {
                Debug.Log("checkReveice");
                if (socketReceiveJob.Update())
                {
                    message = socketReceiveJob.message;
                    Debug.Log(message);
                    if (message != null)
                    {
                        if (message.Contains("startAcquisition"))
                        {
                            Debug.Log(message);
                            state = "startAcquisition";
                        }
                    }
                }
            }
            else if (state.Equals("startAcquisition"))
            {
                socketToParams(message);
                sphereSpeed = sphereSpeed * Mathf.Deg2Rad;
                sphereLimitAngleLimits = sphereLimitAngle;
                sphereLimitAngle = Mathf.PI / 2 - sphereLimitAngle * Mathf.Deg2Rad;
                if (sphereControlScript != null)
                {
                    sphereControlScript.Reset();
                }
                else
                {
                    gameObject.AddComponent<SphereControl>();
                }


                sphereControlScript = gameObject.GetComponent<SphereControl>();
                sphereControlScript.sphereSpeed = sphereSpeed;
                sphereControlScript.sphereLimitAngle = sphereLimitAngle;
                sphereControlScript.sphereWaitTime = sphereWaitTime;
                sphereControlScript.sphereCountdownTime = sphereCountdownTime;
                sphereControlScript.countdownText = countdownText;
                sphereControlScript.sphereRoundTripNumber = sphereRoundTripNumber;


                if (sphereColorScript != null)
                {
                    sphereColorScript.Reset();
                }
                else
                {
                    gameObject.AddComponent<SphereColor>();
                }


                sphereColorScript = gameObject.GetComponent<SphereColor>();
                sphereColorScript.sphereGreenToYellowAngle = sphereGreenToYellowAngle;
                sphereColorScript.sphereYellowToRedAngle = sphereYellowToRedAngle;


                if (acquireMovementScript != null)
                {
                    acquireMovementScript.Reset();
                }
                else
                {
                    gameObject.AddComponent<AcquireMovement>();
                }

                acquireMovementScript = gameObject.GetComponent<AcquireMovement>();
                acquireMovementScript.acquisitionFrequency = acquisitionFrequency;
                acquireMovementScript.profileName = profileName;

                sphereControlScript.acquireMovementScript = acquireMovementScript;

                sphereColorScript.acquireMovementScript = acquireMovementScript;

                if (limitsControlScript != null)
                {
                    limitsControlScript.Reset();
                }
                else
                {
                    gameObject.AddComponent<LimitsControl>();
                }

                limitsControlScript = gameObject.GetComponent<LimitsControl>();
                limitsControlScript.sphereLimitAngle = sphereLimitAngleLimits;

                sphereControlScript.start = true;
                state = "sendStartAcquisitionAck";
                waitedTime = 0.0f;

            } else if (state.Equals("sendStartAcquisitionAck"))
            {
                waitedTime += Time.deltaTime;

                if (waitedTime > waitTime)
                {
                    Debug.Log("connect laaa");
                    connected = SocketClient.connectSocket("127.0.0.1", port);
                    if (connected) {
                        socketReceiveJob = new SocketReceive();
                        port++;

                        SocketClient.socketSend("startAcquisitionAck");
                        socketReceiveJob.Start();
                        state = "checkReceiveOrFinished";
                    }
                    
                }
            }
            else if (state.Equals("checkReceiveOrFinished"))
            {
                if (socketReceiveJob.Update())
                {
                    message = socketReceiveJob.message;
                    if (message != null && !message.Equals(""))
                    {
                        Debug.Log(message);
                        if (message.Equals("stopAcquisition"))
                        {
                            state = "stopAcquisition";
                        }
                        else if (message.Equals("finishAcquisition"))
                        {
                            state = "finishAcquisition";
                        }

                    }
                }
            }
            else if (state.Equals("finishAcquisition"))
            {
                if (sphereControlScript.finished)
                {
                    state = "finished";
                }
            }
            else if (state.Equals("finished"))
            {
                connected = SocketClient.connectSocket("127.0.0.1", port);
                if (connected)
                {
                    port++;
                    SocketClient.socketSend("endAcquisition");

                    state = "receive";
                    waitedTime = 0.0f;
                    float mean = (float)sphereColorScript.acquisitionScore.Sum(x => Convert.ToInt32(x)) / acquireMovementScript.numberOfFrames;
                    Debug.Log(mean);

                    Debug.Log((float) ((float) sphereColorScript.acquisitionScore.Sum(x => (Convert.ToInt32(x) - mean)* (Convert.ToInt32(x) - mean)) /acquireMovementScript.numberOfFrames));
                }
            }
            else if (state.Equals("stopAcquisition"))
            {
                Debug.Log("stopped");
                sphereControlScript.stop = true;

                connected = SocketClient.connectSocket("127.0.0.1", port);

                if (connected)
                {
                    Debug.Log("connected");
                    port++;
                    SocketClient.socketSend("stopAcquisitionAck");
                    state = "receive";
                    waitedTime = 0.0f;
                }

            }
        }


    }

    bool socketToParams(string receivedMessage)
    {
        String[] subMessages = receivedMessage.Split(',');

        foreach (var subMessage in subMessages)
            lineToParam(subMessage);

        return true;
    }


    bool lineToParam(string line)
    {
        if (line != null && !line.Equals("") && line.Contains(":"))
        {
            // Do whatever you need to do with the text line, it's a string now
            // In this example, I split it into arguments based on comma
            // deliniators, then send that array to DoStuff()
            string[] entries = line.Split(':');
            if (entries.Length > 0)
            {
                string param = entries[0];
                string value = entries[1];

                switch (param)
                {
                    case "sphereSpeed":
                        sphereSpeed = float.Parse(value);
                        break;
                    case "sphereLimitAngle":
                        sphereLimitAngle = float.Parse(value);
                        break;
                    case "sphereWaitTime":
                        sphereWaitTime = float.Parse(value);
                        break;
                    case "sphereCountdownTime":
                        sphereCountdownTime = float.Parse(value);
                        break;
                    case "sphereRoundTripNumber":
                        sphereRoundTripNumber = int.Parse(value);
                        break;
                    case "sphereGreenToYellowAngle":
                        sphereGreenToYellowAngle = float.Parse(value);
                        break;
                    case "sphereYellowToRedAngle":
                        sphereYellowToRedAngle = float.Parse(value);
                        break;
                    case "acquisitionFrequency":
                        acquisitionFrequency = int.Parse(value);
                        break;
                    case "profileName":
                        profileName = value;
                        break;
                    default:
                        return false;
                        
                }
                return true;
            }
        }

        return false;
    }


    void LoadConf()
    {
        string line;
        // Create a new StreamReader, tell it which file to read and what encoding the file
        // was saved as
        StreamReader theReader = new StreamReader(confFile, Encoding.Default);
        // Immediately clean up the reader after this block of code is done.
        // You generally use the "using" statement for potentially memory-intensive objects
        // instead of relying on garbage collection.
        // (Do not confuse this with the using directive for namespace at the 
        // beginning of a class!)
        using (theReader)
        {
            // While there's lines left in the text file, do this:
            do
            {
                line = theReader.ReadLine();

                lineToParam(line);
            }
            while (line != null);
            // Done reading, close the reader and return true to broadcast success    
            theReader.Close();
        }
    }

}
