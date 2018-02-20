using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PositionalLock : MonoBehaviour {
    public GameObject cameraGameObject;
 
    // Disable positional tracking by applying an opposite offset from the camera that's being
    // moved by the HMD. This script should be applied on an empty parent object of the camera.
    void Update()
    {
        if (cameraGameObject != null)
        {
            Vector3 offset = new Vector3(
                -cameraGameObject.transform.localPosition.x,
                -cameraGameObject.transform.localPosition.y,
                -cameraGameObject.transform.localPosition.z);
            transform.localPosition = offset;
        }
    }
}
