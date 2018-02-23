using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.Text;
using System.IO;
using System.Net;
using System.Net.Sockets;

/// <summary>
/// A socket client to connect to the Python GUI
/// </summary>
public class SocketClient : MonoBehaviour {
    public static Socket s;

	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		
	}

    /// <summary>
    /// Connects to a socket server
    /// </summary>
    /// <param name="server">Address of the server</param>
    /// <param name="port">Port to connect to</param>
    /// <returns>A boolean, true if the connection succedeed, false if it failed</returns>
    public static bool connectSocket(string server, int port)
    {
        IPAddress address = IPAddress.Parse("127.0.0.1");
        Debug.Log("Connecting to " + server + ":" + port.ToString()+ "...");
        IPEndPoint ipe = new IPEndPoint(address, port);
        Socket tempSocket =
            new Socket(ipe.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
        try
        {
            tempSocket.Connect(ipe);
        } catch
        {
            return false;
        }

        if (tempSocket.Connected)
        {
            s = tempSocket;
            Debug.Log("Connected!");
            return true;
        }
        else
        {
            return false;
        }
        return false;
    }

    /// <summary>
    /// Receive a message from the socket connection
    /// </summary>
    /// <returns>The received message</returns>
    public static string socketReceive()
    {
        Byte[] bytesReceived = new Byte[256];
        int bytes = 0;
        string receivedString = "";
        do
        {
            bytes = s.Receive(bytesReceived, bytesReceived.Length, 0);
            receivedString = receivedString + Encoding.ASCII.GetString(bytesReceived, 0, bytes);
        } while (bytes > 0);
        s.Shutdown(SocketShutdown.Both);
        s.Close();
        return receivedString;
    }

    /// <summary>
    /// Send a message to the socket connection
    /// </summary>
    /// <param name="message">The string message to send</param>
    public static void socketSend(string message)
    {
        Debug.Log("Sending message: " + message);
        Byte[] bytesSent = Encoding.ASCII.GetBytes(message);

        s.Send(bytesSent, bytesSent.Length, 0);
        Debug.Log("Message sent.");
    }

}
