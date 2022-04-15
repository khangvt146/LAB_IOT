using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
 
public class GetTime : MonoBehaviour
{
    public Text time;
    public Text date;

    // Start is called before the first frame update
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
        date.text = System.DateTime.Now.ToString("dd/MM/yyyy");
        time.text = System.DateTime.Now.ToString("HH:mm:ss");
    }
}