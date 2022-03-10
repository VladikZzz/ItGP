using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Movement : MonoBehaviour
{   
    public float speed = 6f;
    public float smoothTime = 0.3F;
    // Update is called once per frame
    void Update()
    {
        float horiz = Input.GetAxis("Horizontal");
        float vert = Input.GetAxis("Vertical");
        Vector3 movementDirection = new Vector3(horiz,0,vert);
        movementDirection.Normalize();
        if(Input.GetKey("w")) {
            transform.position += Time.deltaTime * speed * Vector3.forward; 
        }
        if(Input.GetKey("a")) {
            transform.position += Time.deltaTime * speed * Vector3.left;    
        }
        if(Input.GetKey("s")) {
            transform.position += Time.deltaTime * speed * Vector3.back;             
        }
        if(Input.GetKey("d")) {
            transform.position += Time.deltaTime * speed * Vector3.right;    
        }
        if(Input.GetKey(KeyCode.UpArrow)) {
            transform.position += Time.deltaTime * speed * Vector3.forward;    
        }
        if(Input.GetKey(KeyCode.DownArrow)) {
            transform.position += Time.deltaTime * speed * Vector3.back;    
        }
        if(Input.GetKey(KeyCode.LeftArrow)) {
            transform.position += Time.deltaTime * speed * Vector3.left;    
        }
        if(Input.GetKey(KeyCode.RightArrow)) {
            transform.position += Time.deltaTime * speed * Vector3.right;    
        }
        if(movementDirection != Vector3.zero) {
            transform.forward = movementDirection;
        }
    }
}
