using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    public float Speed = 1f;
    public Vector3 Direction1 = Vector3.forward;
    public Vector3 Direction2 = Vector3.left;
    private int _directionIndex;
    private Rigidbody _rigidbody;

    private void Awake()
    {
        _rigidbody = GetComponent<Rigidbody>();
    }
    private void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            _directionIndex = _directionIndex == 0 ? 1 : 0;
        }
    }
    private void FixedUpdate()
    {
        var velocity = _directionIndex == 0 ? Vector3.forward : Vector3.right;
        velocity = GetDirection() * Speed;
        velocity.y = _rigidbody.velocity.y;
        _rigidbody.velocity = velocity;
    }

    private Vector3 GetDirection()
    {
        if (_directionIndex == 0)
        {
            return Direction1;
        }

        return Direction2;
    }

    private void OnDisable()
    {
        Vector3 velocity = Vector3.zero;
        velocity.y = _rigidbody.velocity.y;
        _rigidbody.velocity = velocity; 
    }
}