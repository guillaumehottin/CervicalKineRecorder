using UnityEngine;
using System.Collections;


/// <summary>
/// Thread class that allows to simply inherit from it to create a simple threaded job
/// To use it, inherit from it and implement the methods ThreadFunction and OnFinished.
/// Thread function is the job that runs when the thread is started and OnFinished is the callback called when the job is finished
/// </summary>
public class ThreadedJob
{
    private bool m_IsDone = false;
    private object m_Handle = new object();
    private System.Threading.Thread m_Thread = null;
    public bool IsDone
    {
        get
        {
            bool tmp;
            lock (m_Handle)
            {
                tmp = m_IsDone;
            }
            return tmp;
        }
        set
        {
            lock (m_Handle)
            {
                m_IsDone = value;
            }
        }
    }

    /// <summary>
    /// Start the thread
    /// </summary>
    public virtual void Start()
    {
        m_Thread = new System.Threading.Thread(Run);
        m_Thread.Start();
    }

    /// <summary>
    /// Cancel the execution of the thread
    /// </summary>
    public virtual void Abort()
    {
        m_Thread.Abort();
    }

    /// <summary>
    /// The logic that will be done by the thread when ran
    /// </summary>
    protected virtual void ThreadFunction() { }

    /// <summary>
    /// The callback function that will be called when the job is done
    /// </summary>
    protected virtual void OnFinished() { }

    /// <summary>
    /// Returns True if the thread is finished, False if it is still running
    /// </summary>
    /// <returns></returns>
    public virtual bool Update()
    {
        if (IsDone)
        {
            OnFinished();
            return true;
        }
        return false;
    }

    /// <summary>
    /// Run the thread
    /// </summary>
    private void Run()
    {
        ThreadFunction();
        IsDone = true;
    }
}