using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FpsLimit : MonoBehaviour {

    public int targetFPS = 30;


	// Use this for initialization
	void Start () {
        QualitySettings.vSyncCount = 0;
        Application.targetFrameRate = targetFPS;
    }

    // Update is called once per frame
    void Update () {
        if (Application.targetFrameRate != targetFPS)
            Application.targetFrameRate = targetFPS;
    }
}
