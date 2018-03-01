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

    public float sphereSpeed; // the speed of the sphere, in degrees/s
    public float sphereLimitAngle; // the maximum angle, in degrees, between 0 and 90
    public float sphereWaitTime; // the time the sphere waits at the borders, in seconds
    public float sphereCountdownTime; // the time to wait at the start of the acquisition, in seconds
    public int sphereRoundTripNumber; // the number of time the sphere does a round trip, starting when the sphere first hits the left border
    public float sphereLimitAngleLimits; // allows to save the limit angles in degrees for later

    public float sphereGreenToYellowAngle; // the angle difference at which the ball gets from green to yellow, in radians
    public float sphereYellowToRedAngle; // the angle difference at which the ball gets from yellow to red, in radians

    public string outputFilePath;
    public int acquisitionFrequency; // the number of time per secondes that the rotation of the headset is acquired

    public string profileName;

    // The different scripts to attach to the Controller game object
    private SphereControl sphereControlScript;
    private SphereColor sphereColorScript;
    private AcquireMovement acquireMovementScript;
    private LimitsControl limitsControlScript;
    private s_TCP sTCPScript;
    private SocketClient socketClientScript;
    private SocketReceive socketReceiveJob;

    // The UI elements to display the text and the crosshair
    public Text countdownText;
    public Image crosshair;


    private string confFile = "cervical.conf"; // the path to the configuration file, for debugging purposes
    private bool conf = false; // true if you want to use the configuration file, false if you want to use the sockets


    public bool receivebool = true;
    public int messages = 0;

    private string message; // the message received from the socket
    private string state; // the state of the script, allows it to go sequentially through all the necessary operations

    private float waitTime = 0.3f; // the wait time before an attempt to connect to the socket server
    private float waitedTime; // the time waited when needed

    private bool connected = false; // a boolean, set to true when the connection to the remote socket server succeeded

    // during the life cycle of the app, we cycle by incrementing the port of the socket we're connecting to
    private int STARTING_PORT = 50007; // the starting port to connect to
    private int ENDING_PORT = 51000; // the ending port to connect to

    private int port; // the port we are using at a given time


    void Start () {
        if (conf) // for debugging purposes, uses the parameters from a given conf file
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
        else // when using the sockets, tells the script to connect to the remote socket server
        {
            state = "connect";
        }
    }
    
    void Update() {
        if (!conf) // only if using the sockets
        {
            if (state.Equals("wait")) // wait before connecting to the socket server
            {
                waitedTime += Time.deltaTime;
                if (waitedTime > waitTime) // if we waited enough, connect to the server at the next frame
                {
                    port = STARTING_PORT;
                    state = "connect";
                }
            }
            else if (state.Equals("connect")) // connect to the socket server
            {
                port = STARTING_PORT;
                connected = SocketClient.connectSocket("127.0.0.1", port);
                if (connected)
                {
                    if (port > ENDING_PORT)
                    {
                        port = STARTING_PORT;
                    }
                    else
                    {
                        port++;
                    }
                    state = "receive"; // go to the receive state to start the acquisition
                    Debug.Log("Waiting for startAcquisition...");
                }

            }
            else if (state.Equals("receive")) // receive a message from the socket
            {
                socketReceiveJob = new SocketReceive();
                socketReceiveJob.Start();

                state = "checkReceive";
            }
            else if (state.Equals("checkReceive")) // check if a message has been received
            {
                if (socketReceiveJob.Update())
                {
                    message = socketReceiveJob.message;
                    if (message != null)
                    {
                        if (message.Contains("startAcquisition"))
                        {
                            state = "startAcquisition"; // correct message, go start the acquisition
                        }
                    }
                }
            }
            else if (state.Equals("startAcquisition")) // start the acquisition
            {
                Debug.Log("Parsing Acquisition parameters...");
                socketToParams(message); // get the parameters from the message
                sphereSpeed = sphereSpeed * Mathf.Deg2Rad;
                sphereLimitAngleLimits = sphereLimitAngle;
                sphereLimitAngle = Mathf.PI / 2 - sphereLimitAngle * Mathf.Deg2Rad;

                // setup the script controlling the sphere
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

                //  setup the script that changes the ball color according to the angle difference from the camera
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

                // setup the script that acquires the head rotation
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

                // setup the scripts that display the lft and right border, showing where the ball will stop
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
                state = "sendStartAcquisitionAck"; // got to send the acknoledgement
                waitedTime = 0.0f;
                Debug.Log("Acquisition started.");

            } else if (state.Equals("sendStartAcquisitionAck")) // send the acknowledgement that we must start the acquisition
            {
                waitedTime += Time.deltaTime;

                if (waitedTime > waitTime) // wait before connecting to the socket server
                {
                    connected = SocketClient.connectSocket("127.0.0.1", port);
                    if (connected) {
                        socketReceiveJob = new SocketReceive();
                        if (port == ENDING_PORT)
                        {
                            port = STARTING_PORT;
                        }
                        else
                        {
                            port++;
                        }

                        SocketClient.socketSend("startAcquisitionAck");
                        socketReceiveJob.Start();
                        state = "checkReceiveOrFinished"; // go wait for the next message
                    }
                    
                }
            }
            else if (state.Equals("checkReceiveOrFinished")) // waiting for 2 messages, either stopAcquisition or finishAcquisition
            {
                if (socketReceiveJob.Update())
                {
                    message = socketReceiveJob.message;
                    if (message != null && !message.Equals(""))
                    {
                        if (message.Equals("stopAcquisition"))
                        {
                            Debug.Log("Stopping acquisition...");
                            state = "stopAcquisition";
                        }
                        else if (message.Equals("finishAcquisition"))
                        {
                            Debug.Log("Finishing acquisition...");
                            state = "finishAcquisition";
                        }

                    }
                }
            }
            else if (state.Equals("finishAcquisition")) // this message means that the acquisition must go to the end
            {
                if (sphereControlScript.finished) // check if it is actually finished every frame
                {
                    Debug.Log("Acquisition finished.");
                    state = "finished";
                }
            }
            else if (state.Equals("finished")) // the acquisition is finished, send the endAcquisition message with the mean and the standard deviation
            {
                connected = SocketClient.connectSocket("127.0.0.1", port);
                if (connected)
                {
                    if (port == ENDING_PORT)
                    {
                        port = STARTING_PORT;
                    }
                    else
                    {
                        port++;
                    }
                    waitedTime = 0.0f;
                    float mean = (float)sphereColorScript.acquisitionScore.Sum(x => Convert.ToInt32(x)) / acquireMovementScript.numberOfFrames;
                    float standardDeviation = (float)((float)sphereColorScript.acquisitionScore.Sum(x => (Convert.ToInt32(x) - mean) * (Convert.ToInt32(x) - mean)) / acquireMovementScript.numberOfFrames);
                   
                    SocketClient.socketSend("endAcquisition,mean:" + mean.ToString() + ",standardDeviation:" + standardDeviation.ToString());

                    state = "receive";
                    Debug.Log("Waiting for startAcquisition...");
                }
            }
            else if (state.Equals("stopAcquisition")) // stop the acquisition and send the stopAcquisition acknowledgement
            {
                Debug.Log("Acquisition stopped.");
                sphereControlScript.stop = true;

                connected = SocketClient.connectSocket("127.0.0.1", port);

                if (connected)
                {
                    if (port == ENDING_PORT)
                    {
                        port = STARTING_PORT;
                    }
                    else
                    {
                        port++;
                    }

                    SocketClient.socketSend("stopAcquisitionAck");
                    state = "receive";
                    waitedTime = 0.0f;
                    Debug.Log("Waiting for startAcquisition...");
                }

            }
        }


    }

    /// <summary>
    /// Initializes the parameters of the aquisition from the startAcquisition message parameters
    /// </summary>
    /// <param name="receivedMessage">The startAcquisition message</param>
    /// <returns></returns>
    bool socketToParams(string receivedMessage)
    {
        String[] subMessages = receivedMessage.Split(',');

        foreach (var subMessage in subMessages)
            lineToParam(subMessage);

        return true;
    }


    /// <summary>
    /// Initializes a parameter from a 'parameter:value' string
    /// </summary>
    /// <param name="line">The line to parse</param>
    /// <returns>True if it went well</returns>
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


    /// <summary>
    /// Initialize the parameters of the acquisition from the configuration file
    /// </summary>
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
