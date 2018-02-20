using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SocketReceive : ThreadedJob
{
    public string message; // arbitary job data

    protected override void ThreadFunction()
    {
        message = SocketClient.socketReceive();
    }
    protected override void OnFinished()
    {
    }
}