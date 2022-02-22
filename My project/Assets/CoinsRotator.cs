using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CoinsRotator : MonoBehaviour
{
    public float amplitude = 0.5f;
    public float frequency = 1f;
 
    // Position Storage Variables
    Vector3 posOffset = new Vector3 ();
    Vector3 tempPos = new Vector3 ();
    void Start () {
        // Store the starting position & rotation of the object
        posOffset = transform.position;
    }
    void Update()
    {
        transform.Rotate(new Vector3(0, 45, 0) * Time.deltaTime);
        tempPos = posOffset;
        tempPos.y += Mathf.Sin (Time.fixedTime * Mathf.PI * frequency) * amplitude;
 
        transform.position = tempPos;
        
    }
}
