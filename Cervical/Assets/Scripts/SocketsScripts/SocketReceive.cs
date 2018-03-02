using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// A thread job to receive a message
/// </summary>
public class SocketReceive : ThreadedJob
{
    public string message; // The message that will be received

    /// <summary>
    /// Receive the message from the thread
    /// </summary>
    protected override void ThreadFunction()
    {
        message = SocketClient.socketReceive();
    }

    /// <summary>
    /// Prints the received message to the Debug consoles
    /// </summary>
    protected override void OnFinished()
    {
        Debug.Log("Received message: " + message);
    }
}