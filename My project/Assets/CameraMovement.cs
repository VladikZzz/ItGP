using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraMovement : MonoBehaviour
{
    public Transform FollowTarget;

    private void Awake()
    {   
        Vector3 InitialPosition = transform.position;
        _offset = InitialPosition - FollowTarget.position;
        _fixedY = InitialPosition.y;
    }

    private float _fixedY;
    private Vector3 _offset;

    private void LateUpdate()
    {
        Vector3 newPosition = FollowTarget.position + _offset;
        newPosition.y = _fixedY;
        transform.position = newPosition;
    }
}