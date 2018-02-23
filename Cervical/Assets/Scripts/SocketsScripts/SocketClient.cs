using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.Text;
using System.IO;
using System.Net;
using System.Net.Sockets;


public class SocketClient : MonoBehaviour {

    public string host = "127.0.0.1";
    public int port = 50007;
    public static Socket s;

	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		
	}

    public static bool connectSocket(string server, int port)
    {
        IPHostEntry hostEntry = null;

        // Get host related information.
        //hostEntry = Dns.GetHostEntry(server);

        // Loop through the AddressList to obtain the supported AddressFamily. This is to avoid
        // an exception that occurs when the host IP Address is not compatible with the address family
        // (typical in the IPv6 case).
        //foreach (IPAddress address in hostEntry.AddressList)
        //{
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
        //}
        return false;
    }

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

    public static void socketSend(string message)
    {
        Byte[] bytesSent = Encoding.ASCII.GetBytes(message);

        s.Send(bytesSent, bytesSent.Length, 0);
    }


    // This method requests the home page content for the specified server.
    public string SocketSendReceive(string server, int port)
    {
        string request = "GET / HTTP/1.1\r\nHost: " + server +
            "\r\nConnection: Close\r\n\r\n";
        Byte[] bytesSent = Encoding.ASCII.GetBytes(request);
        Byte[] bytesReceived = new Byte[256];

        // Create a socket connection with the specified server and port.
        //Socket s = connectSocket(server, port);

        if (s == null)
            return ("Connection failed");


        int bytes = 0;
        string receivedString = "";
        do
        {
            bytes = s.Receive(bytesReceived, bytesReceived.Length, 0);
            receivedString = receivedString + Encoding.ASCII.GetString(bytesReceived, 0, bytes);
        }
        while (bytes > 0);


        // Send request to the server.
        s.Send(bytesSent, bytesSent.Length, 0);

        return receivedString;
    }
}
