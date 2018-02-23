using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// A thread job to receive a message
/// </summary>
public class SocketReceive : ThreadedJob
{
    public string message; // The message that will be received

    protected override void ThreadFunction()
    {
        message = SocketClient.socketReceive();
    }
    protected override void OnFinished()
    {
        Debug.Log("Received message: " + message);
    }
}