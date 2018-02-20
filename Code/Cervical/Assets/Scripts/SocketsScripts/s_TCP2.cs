using UnityEngine;
using System.Collections;
using System;
using System.IO;
using System.Net.Sockets;
using System.Text;
public class s_TCP2 : MonoBehaviour
{
    internal Boolean socketReadyRead = false;
    internal Boolean socketReadyWrite = false;
    TcpClient mySocketRead;
    NetworkStream theStreamRead;
    StreamWriter theWriterRead;
    StreamReader theReaderRead;
    TcpClient mySocketWrite;
    NetworkStream theStreamWrite;
    StreamWriter theWriterWrite;
    StreamReader theReaderWrite;
    String Host = "localhost";
    Int32 Port = 50007;


    void Start() {
    }


    void Update() {
    }


    // **********************************************
    public void setupSocket() {
        try {
            mySocketRead = new TcpClient(Host, Port);
            theStreamRead = mySocketRead.GetStream();
            theStreamRead.ReadTimeout = 1;
            theWriterRead = new StreamWriter(theStreamRead);
            theReaderRead = new StreamReader(theStreamRead);
            socketReadyRead = true;

            mySocketWrite = new TcpClient(Host, Port + 1);
            theStreamWrite = mySocketWrite.GetStream();
            theStreamWrite.ReadTimeout = 1;
            theWriterWrite = new StreamWriter(theStreamWrite);
            theReaderWrite = new StreamReader(theStreamWrite);
            socketReadyWrite = true;
        } catch (Exception e) {
            Debug.Log("Socket error: " + e);
        }
    }


    public void writeSocket(string theLine) {
        if (!socketReadyWrite)
            return;
        String foo = theLine;
        theWriterWrite.Write(foo);
        theWriterWrite.Flush();
    }


    public String readSocket() {
        if (!socketReadyRead)
            return "";
        try {
            return theReaderRead.ReadLine();
        } catch (Exception e) {
            return "";
        }
    }


    public void closeSocket() {
        if (!socketReadyRead || !socketReadyWrite)
            return;
        theWriterRead.Close();
        theReaderRead.Close();
        mySocketRead.Close();
        socketReadyRead = false;
        theWriterWrite.Close();
        theReaderWrite.Close();
        mySocketWrite.Close();
        socketReadyWrite = false;
    }
} // end class s_TCP